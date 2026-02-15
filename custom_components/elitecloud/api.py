"""api.py: API for Elite Cloud integration."""

import asyncio
from collections import defaultdict
from dataclasses import asdict
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Final
from custom_components.elitecloud.data import EliteCloudDeviceConfig
import httpx
import logging

from homeassistant.core import callback
from homeassistant.core import HomeAssistant
from homeassistant.helpers.httpx_client import create_async_httpx_client

from pyelitecloud import (
    AsyncEliteCloudApi,
    EliteCloudApiFlag,
    EliteCloudCmdSection,
    EliteCloudCmdAction,
    EliteCloudConnectError,
    EliteCloudAuthError,
    EliteCloudSite,
) 

from .const import (
    DOMAIN,
    API,
    API_RETRY_ATTEMPTS,
    API_RETRY_DELAY,
    STORE_KEY_CACHE,
    STORE_WRITE_PERIOD_CACHE,
    utcnow,
    utcmin,
)
from .data import (
    EliteCloudDatapoint,
    EliteCloudDeviceConfig,
    EliteCloudDeviceStatus,
)

# Define logger
_LOGGER = logging.getLogger(__name__)

class EliteCloudApiFactory:
    
    @staticmethod
    def create(hass: HomeAssistant, username: str, password: str) -> 'EliteCloudApiWrap':
        """
        Get a stored instance of the EliteCloudApi for given credentials
        """
    
        key = f"{username.lower()}_{hash(password) % 10**8}"
    
        # Sanity check
        if not DOMAIN in hass.data:
            hass.data[DOMAIN] = {}
        if not API in hass.data[DOMAIN]:
            hass.data[DOMAIN][API] = {}
            
        # if a EliteCloudApiWrap instance for these credentials is already available then re-use it
        api = hass.data[DOMAIN][API].get(key, None)

        if not api or api.closed:
            _LOGGER.debug(f"create Api for account '{username}'")
            
            # Create a new EliteCloudApiWrap instance and remember it
            api = EliteCloudApiWrap(hass, username, password)
            hass.data[DOMAIN][API][key] = api
        else:
            _LOGGER.debug(f"reuse Api for account '{username}'")

        return api
    

    @staticmethod
    def create_temp(hass: HomeAssistant, username: str, password: str) -> 'EliteCloudApiWrap':
        """
        Get a temporary instance of the EliteCloudApi for given credentials
        """

        key = f"{username.lower()}_{hash(password) % 10**8}"
    
        # Sanity check
        if not DOMAIN in hass.data:
            hass.data[DOMAIN] = {}
        if not API in hass.data[DOMAIN]:
            hass.data[DOMAIN][API] = {}
            
        # if a EliteCloudApiWrap instance for these credentials is already available then re-use it
        api = hass.data[DOMAIN][API].get(key, None)
        
        if not api or api.closed:
            _LOGGER.debug(f"create temp Api")

            # Create a new EliteCloudApiWrap instance
            api = EliteCloudApiWrap(hass, username, password, is_temp=True)
    
        return api    


    @staticmethod
    async def async_close_temp(api: 'EliteCloudApiWrap'):
        """
        Close a previously created EliteCloudApi
        """
        try:
            if api.is_temp and not api.closed:
                _LOGGER.debug("close temp Api")
                await api.close()

        except Exception as ex:
            _LOGGER.debug("Exception while closing temp Api: {ex}")


class EliteCloudApiWrap(AsyncEliteCloudApi):
    """Wrapper around AsyncEliteCloudApi class"""

    def __init__(self, hass: HomeAssistant, username: str, password: str, is_temp: bool = False):
        """Initialize the api"""

        self._hass = hass
        self._username = username
        self._password = password
        self.is_temp = is_temp

        # Create a fresh http client
        client: httpx.AsyncClient = create_async_httpx_client(hass) 
        
        # Initialize the actual api
        flags = {
            EliteCloudApiFlag.RENEW_HANDLER_START: True if not is_temp else False,
            EliteCloudApiFlag.DIAGNOSTICS_COLLECT: True
        } 
        super().__init__(username, password, client=client, flags=flags)

        # Data properties
        self.devices_changed: bool = False
        self.devices: dict[str,EliteCloudDeviceConfig] = {}
        self.status: dict[str, EliteCloudDeviceStatus] = {}

        # Coordinator listener to report back any changes in the data
        self._async_data_listener = None

        # For diagnostics
        self._diag_values = defaultdict(set)


    def set_initial_devices(self, device_configs: list[EliteCloudDeviceConfig]):
        """
        Set initial devices from config_entry so we can subscribe to updates before we've done a poll
        """
        for device_config in device_configs:
            site = EliteCloudSite(
                uuid = device_config.uuid,
                name = device_config.name,
                panel_mac = device_config.mac,
                panel_serial = device_config.serial
            )
            self._sites.append(site)    # in super class AsyncEliteCloudApi
            self.devices[device_config.uuid] = device_config


    async def async_detect_data(self, force_relogin:bool = False, verbose:bool = False):
        """
        We mostly rely on the remote servers notifying us of changes of data (push).
        However, we do an infrequent periodical poll to detect added or removed devices.
        """
        # Logout so we really force a subsequent login and not use an old token
        if force_relogin:
            await self._async_logout()
    
        # Login
        await self._async_login()

        # Fetch the all sites (=devices)
        await self._async_poll_sites(verbose=verbose)
        await self._async_poll_sites_statusses(verbose=verbose)
    

    async def _async_login(self):
        """Login"""
        await super().login()
        

    async def _async_logout(self):
        """Logout"""
        await super().logout()


    async def _async_poll_sites(self, verbose:bool = False):
        """
        Attempt to refresh the list of sites
        """
        old_device_ids = set( self.devices.keys() )
        new_device_ids = set()

        sites = await super().fetch_sites()
        if verbose:
            _LOGGER.debug(f"found sites data: {sites}")

        for site in sites:
            site_uuid = site.get('uuid')
            site_resources = await super().fetch_site_resources(site_uuid)
            if verbose:
                _LOGGER.debug(f"found resources for site {site_uuid}: {site_resources}")

            # Parse the data
            site["resources"] = site_resources
            device = EliteCloudDeviceConfig.from_data(site)

            # Check for changes. Note that we only trigger on new or changed device, not on removed device
            old_device = self.devices.get(device.uuid)
            if old_device is None:
                _LOGGER.info(f"Detected new device '{device.name}' ({device.uuid}) for account {self._username}")
                self.devices_changed = True

            elif device != old_device:
                _LOGGER.info(f"Detected change in device '{device.name}' ({device.uuid}) for account {self._username}")
                self.devices_changed = True

            # Store the new device config
            self.devices[device.uuid] = device
            new_device_ids.add(device.uuid)

        # cleanup
        for id in old_device_ids:
            if not id in new_device_ids:
                self.devices.pop(id, '')


    async def _async_poll_sites_statusses(self, verbose:bool = False):
        """
        Fetch statusses for all sites
        """
        old_status_ids = set( self.status.keys() )
        new_status_ids = set()

        for site_uuid in self.devices.keys():
            site_status = await super().fetch_site_status(site_uuid)

            if verbose:
                _LOGGER.debug(f"found status for site {site_uuid}: {site_status}")

            device_status = EliteCloudDeviceStatus.from_data(site_uuid, site_status)
            self.status[device_status.uuid] = device_status
            new_status_ids.add(device_status.uuid)

            # Keep track of status values seen
            await self._async_update_diagnostics(device_status=device_status)

        # Cleanup
        for id in old_status_ids:
            if not id in new_status_ids:
                self.status.pop(id,'')


    async def async_toggle_datapoint(self, device: EliteCloudDeviceConfig, datapoint: EliteCloudDatapoint):
        """
        Send a toggle command to an input or output
        """
        site_uuid = device.uuid
        id = datapoint.id
        section = EliteCloudCmdSection(datapoint.sec)
        action = EliteCloudCmdAction.TOGGLE

        await super().send_site_command(site_uuid, section, id, action)


    async def async_subscribe_to_push_data(self, callback):
        """
        Subscribe to changes in site status.
        """
        try:
            # Remember how to report back data changes to the coordinator
            self._async_data_listener = callback

            # Register listeners for changes in remote data
            for site in self._sites:
                await super().subscribe_site_status(site.uuid, self._on_site_status_change)

        except Exception as e:
            _LOGGER.info(f"{e}")


    async def _on_site_status_change(self, site: EliteCloudSite, section:str, idx:str, status: dict):
        """
        Handle updated site status or partial status received from the remote servers
        """
        try:
            # Actual changed data is already stored in super()._sites_status[site.uuid]
            site_status = self._sites_status.get(site.uuid)

            device_status = EliteCloudDeviceStatus.from_data(site.uuid, site_status)
            self.status[device_status.uuid] = device_status
            
            # Keep track of status values seen
            await self._async_update_diagnostics(device_status=device_status)

            # Signal to the coordinator that there were changes in the api data
            if self._async_data_listener is not None:
                await self._async_data_listener()

        except Exception as e:
            _LOGGER.info(f"{e}")


    async def _async_update_diagnostics(self, device_status:EliteCloudDeviceStatus=None):
        """
        Update diagnostics
        """
        # Keep track of status values seen. Results in dict[key,list[val]]
        if device_status is not None:
            for key,val in device_status._statuses.items():
                self._diag_values[key].add(val)


    async def async_get_diagnostics(self) -> dict[str, Any]:

        diag = super().diagnostics

        diag["data"].update( {
            "devices": [ asdict(d) for d in self.devices.values() ],
            "status": [ asdict(s) for s in self.status.values() ],
            "values": self._diag_values,
        } )
        return diag
   






