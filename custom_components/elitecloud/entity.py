import logging
import re

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.number import NumberDeviceClass
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorStateClass
from homeassistant.const import EntityCategory
from homeassistant.const import PERCENTAGE
from homeassistant.const import SIGNAL_STRENGTH_DECIBELS
from homeassistant.const import SIGNAL_STRENGTH_DECIBELS_MILLIWATT
from homeassistant.const import UnitOfInformation
from homeassistant.const import UnitOfElectricCurrent
from homeassistant.const import UnitOfElectricPotential
from homeassistant.const import UnitOfEnergy
from homeassistant.const import UnitOfLength
from homeassistant.const import UnitOfPower
from homeassistant.const import UnitOfPressure
from homeassistant.const import UnitOfVolume
from homeassistant.const import UnitOfVolumeFlowRate
from homeassistant.const import UnitOfTemperature
from homeassistant.const import UnitOfTime
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.restore_state import ExtraStoredData, RestoreEntity

from .const import (
    DOMAIN,
    ATTR_DATA_VALUE,
    ATTR_STORED_DATA_VALUE,
    PREFIX_ID,
    utcnow,
)
from .coordinator import (
    EliteCloudCoordinator,
)
from .data import (
    EliteCloudDatapoint,
    EliteCloudDeviceConfig,
    EliteCloudDeviceResource,
)

# Define logger
_LOGGER = logging.getLogger(__name__)


@dataclass
class EliteCloudEntityExtraData(ExtraStoredData):
    """Object to hold extra stored data."""
    data_value: Any = None
    
    def as_dict(self) -> dict[str, Any]:
        """Return a dict representation of the sensor data."""
        return {
            ATTR_STORED_DATA_VALUE: self.data_value
        }

    @classmethod
    def from_dict(cls, restored: dict[str, Any]) -> Self | None:
        """Initialize a stored sensor state from a dict."""
        return cls(
            data_value = restored.get(ATTR_STORED_DATA_VALUE)
        )


class EliteCloudEntity(RestoreEntity):
    """
    Common funcionality for all Entities:
    (EliteCloudSensor, EliteCloudBinarySensor, ...)
    """
    
    def __init__(self, coordinator: EliteCloudCoordinator, device: EliteCloudDeviceConfig, resource: EliteCloudDeviceResource, datapoint: EliteCloudDatapoint):

        # Remember the static meta parameters for this entity
        self._coordinator = coordinator
        self._device = device
        self._resource = resource
        self._datapoint = datapoint

        # The unique identifiers for this sensor within Home Assistant
        self.object_id       = EliteCloudEntity.create_id(PREFIX_ID, device.uuid, datapoint.key) # elitecontrol_<device_uuid>_<key>
        self._attr_unique_id = EliteCloudEntity.create_id(PREFIX_ID, device.name, datapoint.key) # elitecontrol_<device_name>_<key>

        self._attr_has_entity_name = True
        self._attr_name = resource.name 
        self._name = resource.name

        self._attr_entity_registry_enabled_default = resource.is_active and not resource.is_hidden

        # Attributes to be restored in the next HA run
        self._data_value: Any = None     # Original data value as returned from Api

        # Derived properties
        self._unit = self.get_unit()        # don't apply directly to _attr_unit, some entities don't have it
        self._attr_icon = self.get_icon()

        self._attr_entity_registry_enabled_default = self.get_entity_enabled_default()
        self._attr_entity_category = self.get_entity_category()

        # Link to the device
        self._attr_device_info = DeviceInfo(
            identifiers = {(DOMAIN, device.uuid)},
        )


    @property
    def suggested_object_id(self) -> str | None:
        """Return input for object id."""
        return self.object_id


    @property
    def extra_state_attributes(self) -> dict[str, str | list[str]]:
        """
        Return the state attributes to display in entity attributes.
        """
        state_attr = {}

        if self._data_value is not None:
            state_attr[ATTR_DATA_VALUE] = self._data_value

        return state_attr        


    @property
    def extra_restore_state_data(self) -> EliteCloudEntityExtraData | None:
        """
        Return entity specific state data to be restored on next HA run.
        """
        return EliteCloudEntityExtraData(
            data_value = self._data_value
        )
    

    @staticmethod
    def create_id(*args):
        s = '_'.join(str(item) for item in args if item is not None).strip('_')
        s = re.sub('[ -]', '_', s)
        s = re.sub('[^a-z0-9_]+', '', s.lower())
        return s            
    
    
    async def async_added_to_hass(self) -> None:
        """
        Handle when the entity has been added
        """
        await super().async_added_to_hass()

        # Get last data from previous HA run                      
        last_state = await self.async_get_last_state()
        last_extra = await self.async_get_last_extra_data()

        if last_state and last_extra:
            # Get entity value from restored data
            dict_extra = last_extra.as_dict()
            data_value = dict_extra.get(ATTR_STORED_DATA_VALUE)

            self._update_value(data_value, force=True)
    

    def _update_value(self, data_value: Any, force:bool=False) -> bool:
        """
        Process any changes in value
        
        To be extended by derived entities
        """
        changed = False

        if force or self._data_value != data_value:

            self._data_value = data_value
            self._attr_icon = self.get_icon()
            changed = True


        return changed


    def get_unit(self):
        """Convert from Datapoint unit abbreviation to Home Assistant units"""
        if self._datapoint is None:
            return None
        
        match self._datapoint.unit:
            case '' | None: return None
            
            case _:
                _LOGGER.warning(f"Encountered a unit or measurement '{self._datapoint.unit}' for '{self._datapoint.key}' that may not be supported by Home Assistant. Please contact the integration developer to have this resolved.")
                return self._datapoint.unit
    
        
    def get_icon(self):
        """Return appropriate icon"""

        # Specific check for the 'snooze sensor x' switches
        if self._datapoint.key.startswith("snooze"):    
            return 'mdi:pause-circle' if self._data_value=="bypass" else 'mdi:play-circle'

        # For Sensors
        match self._data_value:
            case "bypass": return 'mdi:pause-circle'
            case _:        return None      # icon is determined by device_class
    
    
    def get_binary_sensor_device_class(self):
        """Return one of the BinarySensorDeviceClass.xyz or None"""
        match self._datapoint.sec:
            case 'area':     return None                            # On/Off
            case 'output':   return None                            # On/Off
            case 'tamper':   return BinarySensorDeviceClass.PROBLEM # or TAMPER: Tamper/clear
            case 'system':   return BinarySensorDeviceClass.PROBLEM # problem/ok
            case 'keypad':   return BinarySensorDeviceClass.PROBLEM # problem/ok

        match self._resource.icon:
            case 'ic_s_running':     return BinarySensorDeviceClass.MOTION
            case 'ic_s_detect_body': return BinarySensorDeviceClass.MOTION
            case 'ic_s_detect_bottom': return BinarySensorDeviceClass.MOTION
            case 'ic_s_detect_top': return BinarySensorDeviceClass.MOTION
            case 'ic_s_detect_co2': return BinarySensorDeviceClass.CO
            case 'ic_s_detect_fire': return BinarySensorDeviceClass.SMOKE
            case 'ic_s_detect_odor': return BinarySensorDeviceClass.GAS
            case 'ic_s_window_closes': return BinarySensorDeviceClass.WINDOW
            case 'ic_s_window_open': return BinarySensorDeviceClass.WINDOW
            case 'ic_s_door_closed': return BinarySensorDeviceClass.DOOR
            case 'ic_s_front_door_open': return BinarySensorDeviceClass.DOOR
            case 'ic_s_front_door_closed': return BinarySensorDeviceClass.DOOR
            case 'ic_s_room_door_open': return BinarySensorDeviceClass.DOOR
            case 'ic_s_room_door_closed': return BinarySensorDeviceClass.DOOR
            case 'ic_s_double_swing_gate_open': return BinarySensorDeviceClass.DOOR
            case 'ic_s_double_swing_gate_closed': return BinarySensorDeviceClass.DOOR
            case 'ic_s_double_sliding_gate_open': return BinarySensorDeviceClass.DOOR
            case 'ic_s_single_sliding_gate_open': return BinarySensorDeviceClass.DOOR
            case 'ic_s_pedestrian_gate': return BinarySensorDeviceClass.DOOR
            case 'ic_s_garage_open': return BinarySensorDeviceClass.GARAGE_DOOR
            case 'ic_s_garage_closing': return BinarySensorDeviceClass.GARAGE_DOOR
            case 'ic_s_garage_half_open': return BinarySensorDeviceClass.GARAGE_DOOR
            case 'ic_s_garage_closed': return BinarySensorDeviceClass.GARAGE_DOOR
            case 'ic_s_storage': return BinarySensorDeviceClass.GARAGE_DOOR
            case 'ic_s_door_lock': return BinarySensorDeviceClass.LOCK
            case 'ic_s_card_door_lock': return BinarySensorDeviceClass.LOCK
            case 'ic_s_padlock': return BinarySensorDeviceClass.LOCK
            case 'ic_s_thermometer': return BinarySensorDeviceClass.HEAT

        return None

    
    def get_entity_category(self):
        # Return EntityCategory as configured in DATASET
        match self._datapoint.flag_category:
            case "conf":    return EntityCategory.CONFIG
            case "diag":    return EntityCategory.DIAGNOSTIC
            case "none":    return None
            case _:         return None


    def get_entity_enabled_default(self):
        # Return EntityEnabled as configured in DATASET
        match self._datapoint.flag_enabled:
            case 'd': return False
            case 'e': return True
            case _:   return True

