import asyncio
import logging
import math
from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant import exceptions
from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.switch import ENTITY_ID_FORMAT
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.const import CONF_UNIQUE_ID
from homeassistant.const import EntityCategory
from homeassistant.const import Platform
from homeassistant.const import STATE_ON
from homeassistant.const import STATE_OFF
from homeassistant.core import HomeAssistant
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.exceptions import IntegrationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity_registry import async_get
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from datetime import datetime
from datetime import timezone
from datetime import timedelta

from collections import defaultdict
from collections import namedtuple

from .const import (
    SWITCH_VALUES_ON,
    SWITCH_VALUES_OFF,
    utcnow,
)
from .coordinator import (
    EliteCloudCoordinator,
)
from .data import (
    EliteCloudDatapoint,
    EliteCloudDeviceConfig,
    EliteCloudDeviceResource,
    EliteCloudDeviceStatus,
)
from .entity import (
    EliteCloudEntity,
)
from .helper import (
    EliteCloudEntityHelper,
)


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """
    Setting up the adding and updating of binary_sensor entities
    """
    await EliteCloudEntityHelper(hass, config_entry).async_setup_entry(Platform.SWITCH, EliteCloudSwitch, async_add_entities)


class EliteCloudSwitch(CoordinatorEntity, SwitchEntity, EliteCloudEntity):
    """
    Representation of an entity that is part of a gateway, tank or pump.
    """

    def __init__(self, coordinator: EliteCloudCoordinator, device: EliteCloudDeviceConfig, resource: EliteCloudDeviceResource, datapoint: EliteCloudDatapoint) -> None:
        """ 
        Initialize the sensor. 
        """
        CoordinatorEntity.__init__(self, coordinator)
        EliteCloudEntity.__init__(self, coordinator, device, resource, datapoint)
        
        # The unique identifiers for this sensor within Home Assistant
        self.entity_id = ENTITY_ID_FORMAT.format(self._attr_unique_id)   # Device.name + params.key

        # update creation-time only attributes
        self._attr_entity_category = self.get_entity_category()
        self._attr_device_class = SwitchDeviceClass.SWITCH

        # Create all value related attributes (but with unknown value).
        # After this constructor ends, base class EliteCloudEntity.async_added_to_hass() will 
        # set the value using the restored value from the last HA run. Or otherwise it will
        # be set when the first push-data is received.
        self._update_value(None, force=True)

    
    @callback
    def _handle_coordinator_update(self) -> None:
        """
        Handle updated data from the coordinator.
        """

        # find the correct device corresponding to this sensor
        data:dict[str, EliteCloudDeviceStatus] = self._coordinator.data
        status = data.get(self._device.uuid) if data is not None else None
        value = status.get(self._datapoint.key) if status is not None else None

        # Update value related attributes
        if self._update_value(value):
            self.async_write_ha_state()
    
    
    def _update_value(self, data_value: Any, force:bool=False) -> bool:
        """
        Set entity value, unit and icon
        """
        changed = super()._update_value(data_value, force)

        # Convert from EliteCloud data value to Home Assistant attributes
        if data_value in SWITCH_VALUES_ON:
            is_on = True
        elif data_value in SWITCH_VALUES_OFF:
            is_on = False
        else:
            is_on = None

        # Update Home Assistant attributes
        if force or self._attr_is_on != is_on:
            
            self._attr_is_on = is_on
            changed = True
        
        return changed
    

    async def async_turn_on(self, **kwargs) -> None:
        """
        Turn the entity on.
        """

        # Already on?
        data:dict[str, EliteCloudDeviceStatus] = self._coordinator.data
        status = data.get(self._device.uuid) if data is not None else None
        value = status.get(self._datapoint.key) if status is not None else None

        if value in SWITCH_VALUES_ON:
            return
        
        # Toggle from Off to On
        await self.async_toggle()
    
    
    async def async_turn_off(self, **kwargs) -> None:
        """
        Turn the entity off.
        """

        # Already off?
        data:dict[str, EliteCloudDeviceStatus] = self._coordinator.data
        status = data.get(self._device.uuid) if data is not None else None
        value = status.get(self._datapoint.key) if status is not None else None

        if value in SWITCH_VALUES_OFF:
            return
        
        # Toggle from On to Off
        await self.async_toggle()


    async def async_toggle(self, **kwargs) -> None:
        """
        Toggle the switch from On to Off or from Off to On
        """
        status = await self._coordinator.async_toggle_datapoint(self._device, self._datapoint)
        if status is not None:
            self._update_value(status, force=True)
            self.async_write_ha_state()
    