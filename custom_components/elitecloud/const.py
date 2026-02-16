"""Constants for the Elite Cloud integration."""
from datetime import datetime, timezone
import logging

from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
)
from homeassistant.const import Platform


_LOGGER: logging.Logger = logging.getLogger(__package__)


# Base component constants
DOMAIN = "elitecloud"
NAME = "Elite Cloud"
ISSUE_URL = "https://github.com/ankohanse/hass-elite-cloud/issues"

# Map platform to pf codes for both enabled and disabled entities
PLATFORM_TO_PF: dict[Platform, str] = {
    Platform.ALARM_CONTROL_PANEL: "alm",
    Platform.BINARY_SENSOR: "bin",
    Platform.SWITCH: "sw",
}
PLATFORMS = list(PLATFORM_TO_PF.keys())

HUB = "Hub"
API = "Api"
COORDINATOR = "Coordinator"

DEFAULT_USERNAME = ""
DEFAULT_PASSWORD = ""

CONF_SITE_UUID = "site_uuid"
CONF_SITE_NAME = "site_name"

DIAGNOSTICS_REDACT = { CONF_PASSWORD, 'client_secret' }

# To compose entity unique id and names
MANUFACTURER = "Arrowhead Alarm Products"
PREFIX_ID = "elitecloud"
PREFIX_NAME = "Elite Cloud"

# Extra attributes displayed in entity attributes
ATTR_DATA_VALUE = "elitecontrol_value"

# Extra attributes that are restored from the previous HA run
ATTR_STORED_DATA_VALUE = "value"

BINARY_SENSOR_VALUES_ON = [True, 1, '1', 'on', 'open']
BINARY_SENSOR_VALUES_OFF = [False, 0, '0', '', 'off', 'sealed']
BINARY_SENSOR_VALUES_ALL = BINARY_SENSOR_VALUES_ON + BINARY_SENSOR_VALUES_OFF

SWITCH_VALUES_ON = ['on', 'bypass']
SWITCH_VALUES_OFF = ['', 'off', 'bypass cleared', 'open', 'sealed']
SWITCH_VALUES_ALL = SWITCH_VALUES_ON + SWITCH_VALUES_OFF

API_RETRY_ATTEMPTS = 2
API_RETRY_DELAY = 5    # seconds

COORDINATOR_POLLING_INTERVAL = 1*60*60   # 1 hour in seconds
COORDINATOR_RELOAD_DELAY = 1*60*60 # 1 hour in seconds
COORDINATOR_RELOAD_DELAY_MAX = 24*60*60 # 24 hours in seconds

STORE_KEY_CACHE = "cache"
STORE_WRITE_PERIOD_CACHE = 30*60 # 30 minutes in seconds

STATUS_VALIDITY_PERIOD = 15*60 # 15 minutes in seconds

# Global helper functions
utcnow = lambda: datetime.now(timezone.utc)
utcmin = lambda: datetime.min.replace(tzinfo=timezone.utc)
utcmax = lambda: datetime.max.replace(tzinfo=timezone.utc)


