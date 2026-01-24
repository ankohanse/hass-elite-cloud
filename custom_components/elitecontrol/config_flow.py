"""config_flow.py: Config flow for Elite Control integration."""
from __future__ import annotations

from dataclasses import asdict
import logging
import re
from typing import Any

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant import config_entries, exceptions

from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.exceptions import IntegrationError
from homeassistant.helpers.selector import selector

from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_DEVICES,
)

from pyelitecloud import (
    EliteCloudError,
    EliteCloudAuthError,
) 


from .const import (
    DOMAIN,
    DEFAULT_USERNAME,
    DEFAULT_PASSWORD,
)

from .coordinator import (
    EliteControlCoordinatorFactory,
    EliteControlCoordinator,
)
from .data import (
    EliteControlDeviceConfig,
)

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register("elitecontrol")
class ConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""
    
    VERSION = 1
    
    def __init__(self):
        """Initialize config flow."""
        self._username: str = None
        self._password:str = None
        self._errors = {}

        self._device_map: dict[str,EliteControlDeviceConfig] = None

        # Assign the HA configured log level of this module to the pyelitecloud module
        log_level: int = _LOGGER.getEffectiveLevel()
        lib_logger: logging.Logger = logging.getLogger("pyelitecloud")
        lib_logger.setLevel(log_level)

        _LOGGER.info(f"Logging at {logging.getLevelName(log_level)}")
    
    
    async def async_try_connection(self):
        """Test the username and password by connecting to the Elite Cloud servers"""
        _LOGGER.info("Trying connection...")
        
        self._errors = {}
        coordinator = EliteControlCoordinatorFactory.create_temp(self._username, self._password)
        try:
            # Call the EliteCloudApi with the detect_device method
            self._device_map = await coordinator.async_config_flow_data()
            
            if self._device_map is None or len(self._device_map)==0:
                self._errors[CONF_USERNAME] = f"No devices detected"

            else:
                _LOGGER.info("Successfully connected!")
                for device in self._device_map.values():
                    _LOGGER.debug(f"Device {device.name} ({device.uuid}): {device}")

                self._errors = {}
                return True
        
        except EliteCloudError as e:
            self._errors[CONF_PASSWORD] = f"Failed to connect to Elite Cloud servers"
        except EliteCloudAuthError as e:
            self._errors[CONF_PASSWORD] = f"Authentication failed"
        except Exception as e:
            self._errors[CONF_PASSWORD] = f"Unknown error: {e}"

        finally:
            await EliteControlCoordinatorFactory.async_close_temp(coordinator)
        
        return False
    

    # This is step 1 for the user/pass function.
    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle a flow initialized by the user."""
        
        if user_input is not None:
            _LOGGER.debug(f"Step user - handle input {user_input}")
            
            self._username = user_input.get(CONF_USERNAME, '')
            self._password = user_input.get(CONF_PASSWORD, '')
            
            # test the username+password and retrieve the sites for this user
            await self.async_try_connection()
            
            if not self._errors:
                # go to the second step to choose which site to use
                return await self.async_step_finish()
        
        # Show the form with the username+password
        _LOGGER.debug(f"Step user - show form")
        
        return self.async_show_form(
            step_id = "user", 
            data_schema = vol.Schema({
                vol.Required(CONF_USERNAME, description={"suggested_value": self._username or DEFAULT_USERNAME}): str,
                vol.Required(CONF_PASSWORD, description={"suggested_value": self._password or DEFAULT_PASSWORD}): str,
            }),
            errors = self._errors
        )
    
    
    async def async_step_finish(self, user_input=None) -> FlowResult:
        """Configuration has finished"""
        

        # Use username as unique_id for this config flow to avoid the same hub being setup twice
        _LOGGER.debug(f"Step finish - set_unique_id")

        await self.async_set_unique_id(f"{DOMAIN}_{self._username}")
        self._abort_if_unique_id_configured()
    
        # Create the integration entry
        _LOGGER.debug(f"Step finish - create config_entry")

        return self.async_create_entry(
            title = self._username, 
            data = {
                CONF_USERNAME: self._username,
                CONF_PASSWORD: self._password,
            },
            options = {
                CONF_DEVICES: [asdict(d) for d in self._device_map.values()],
            }
        )
    
