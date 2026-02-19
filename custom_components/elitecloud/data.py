import logging

from dataclasses import asdict, dataclass
from enum import StrEnum
from jsonata import Jsonata
from typing import Any

from homeassistant.const import Platform

from .const import (
    PLATFORM_TO_PF,
)


# Define logger
_LOGGER = logging.getLogger(__name__)


@dataclass
class DP:
    key: str            # Unique key for this datapoint
    sec: str            # section (area, input, output, ...)
    id: int             # id within section
    name: str           # Friendly name, used as default when no name is returned in resources.
    pf: str             # Target platform abbreviation; Sensor, Binary_Sensor, Switch, Alarm, etc. If None then not added as entity but may be used internally
    flag: str           # Comma separated flags: enabled/disabled (e or d), entity category (conf, diag or none), default name (dnm)
    rpath: str          # Path for resource params within responses from remote server
    spath: str          # Path for status value within responses from remote server. Note the offset between idx and id!
    fmt: type           # Data format (s=str, b=bool, i=int, t=timestamp, f[n]=float with precision)
    unit: str           # Data unit of measurement
    opt: dict[str,Any]  # Options for Enums

DATAPOINTS = [
    DP(key="area_a",     sec="area",   id=1,  name="area A",     pf="alm", flag="e,none",  rpath="area[idx=0]",    spath="area[id=1].status",   fmt="s",  unit="",  opt={}),
    DP(key="area_b",     sec="area",   id=2,  name="area B",     pf="alm", flag="e,none",  rpath="area[idx=1]",    spath="area[id=2].status",   fmt="s",  unit="",  opt={}),
    DP(key="area_c",     sec="area",   id=3,  name="area C",     pf="alm", flag="e,none",  rpath="area[idx=2]",    spath="area[id=3].status",   fmt="s",  unit="",  opt={}),
    DP(key="area_d",     sec="area",   id=4,  name="area D",     pf="alm", flag="e,none",  rpath="area[idx=3]",    spath="area[id=4].status",   fmt="s",  unit="",  opt={}),
    DP(key="area_e",     sec="area",   id=5,  name="area E",     pf="alm", flag="e,none",  rpath="area[idx=4]",    spath="area[id=5].status",   fmt="s",  unit="",  opt={}),
    DP(key="area_f",     sec="area",   id=6,  name="area F",     pf="alm", flag="e,none",  rpath="area[idx=5]",    spath="area[id=6].status",   fmt="s",  unit="",  opt={}),
    DP(key="area_g",     sec="area",   id=7,  name="area G",     pf="alm", flag="e,none",  rpath="area[idx=6]",    spath="area[id=7].status",   fmt="s",  unit="",  opt={}),
    DP(key="area_h",     sec="area",   id=8,  name="area H",     pf="alm", flag="e,none",  rpath="area[idx=7]",    spath="area[id=8].status",   fmt="s",  unit="",  opt={}),
    DP(key="area_i",     sec="area",   id=9,  name="area I",     pf="alm", flag="e,none",  rpath="area[idx=8]",    spath="area[id=9].status",   fmt="s",  unit="",  opt={}),
    DP(key="area_j",     sec="area",   id=10, name="area J",     pf="alm", flag="e,none",  rpath="area[idx=9]",    spath="area[id=10].status",  fmt="s",  unit="",  opt={}),
    DP(key="area_k",     sec="area",   id=11, name="area K",     pf="alm", flag="e,none",  rpath="area[idx=10]",   spath="area[id=11].status",  fmt="s",  unit="",  opt={}),
    DP(key="area_l",     sec="area",   id=12, name="area L",     pf="alm", flag="e,none",  rpath="area[idx=11]",   spath="area[id=12].status",  fmt="s",  unit="",  opt={}),
    DP(key="area_m",     sec="area",   id=13, name="area M",     pf="alm", flag="e,none",  rpath="area[idx=12]",   spath="area[id=13].status",  fmt="s",  unit="",  opt={}),
    DP(key="area_n",     sec="area",   id=14, name="area N",     pf="alm", flag="e,none",  rpath="area[idx=13]",   spath="area[id=14].status",  fmt="s",  unit="",  opt={}),
    DP(key="area_o",     sec="area",   id=15, name="area O",     pf="alm", flag="e,none",  rpath="area[idx=14]",   spath="area[id=15].status",  fmt="s",  unit="",  opt={}),
    DP(key="area_p",     sec="area",   id=16, name="area P",     pf="alm", flag="e,none",  rpath="area[idx=15]",   spath="area[id=16].status",  fmt="s",  unit="",  opt={}),

    DP(key="sensor_1",   sec="input",  id=1,  name="Sensor 1",   pf="bin", flag="e,none",  rpath="input[idx=0]",   spath="input[id=1].status",  fmt="s",  unit="",  opt={}),
    DP(key="sensor_2",   sec="input",  id=2,  name="Sensor 2",   pf="bin", flag="e,none",  rpath="input[idx=1]",   spath="input[id=2].status",  fmt="s",  unit="",  opt={}),
    DP(key="sensor_3",   sec="input",  id=3,  name="Sensor 3",   pf="bin", flag="e,none",  rpath="input[idx=2]",   spath="input[id=3].status",  fmt="s",  unit="",  opt={}),
    DP(key="sensor_4",   sec="input",  id=4,  name="Sensor 4",   pf="bin", flag="e,none",  rpath="input[idx=3]",   spath="input[id=4].status",  fmt="s",  unit="",  opt={}),
    DP(key="sensor_5",   sec="input",  id=5,  name="Sensor 5",   pf="bin", flag="e,none",  rpath="input[idx=4]",   spath="input[id=5].status",  fmt="s",  unit="",  opt={}),
    DP(key="sensor_6",   sec="input",  id=6,  name="Sensor 6",   pf="bin", flag="e,none",  rpath="input[idx=5]",   spath="input[id=6].status",  fmt="s",  unit="",  opt={}),
    DP(key="sensor_7",   sec="input",  id=7,  name="Sensor 7",   pf="bin", flag="e,none",  rpath="input[idx=6]",   spath="input[id=7].status",  fmt="s",  unit="",  opt={}),
    DP(key="sensor_8",   sec="input",  id=8,  name="Sensor 8",   pf="bin", flag="e,none",  rpath="input[idx=7]",   spath="input[id=8].status",  fmt="s",  unit="",  opt={}),
    DP(key="sensor_9",   sec="input",  id=9,  name="Sensor 9",   pf="bin", flag="e,none",  rpath="input[idx=8]",   spath="input[id=9].status",  fmt="s",  unit="",  opt={}),
    DP(key="sensor_10",  sec="input",  id=10, name="Sensor 10",  pf="bin", flag="e,none",  rpath="input[idx=9]",   spath="input[id=10].status", fmt="s",  unit="",  opt={}),
    DP(key="sensor_11",  sec="input",  id=11, name="Sensor 11",  pf="bin", flag="e,none",  rpath="input[idx=10]",  spath="input[id=11].status", fmt="s",  unit="",  opt={}),
    DP(key="sensor_12",  sec="input",  id=12, name="Sensor 12",  pf="bin", flag="e,none",  rpath="input[idx=11]",  spath="input[id=12].status", fmt="s",  unit="",  opt={}),
    DP(key="sensor_13",  sec="input",  id=13, name="Sensor 13",  pf="bin", flag="e,none",  rpath="input[idx=12]",  spath="input[id=13].status", fmt="s",  unit="",  opt={}),
    DP(key="sensor_14",  sec="input",  id=14, name="Sensor 14",  pf="bin", flag="e,none",  rpath="input[idx=13]",  spath="input[id=14].status", fmt="s",  unit="",  opt={}),
    DP(key="sensor_15",  sec="input",  id=15, name="Sensor 15",  pf="bin", flag="e,none",  rpath="input[idx=14]",  spath="input[id=15].status", fmt="s",  unit="",  opt={}),
    DP(key="sensor_16",  sec="input",  id=16, name="Sensor 16",  pf="bin", flag="e,none",  rpath="input[idx=15]",  spath="input[id=16].status", fmt="s",  unit="",  opt={}),

    DP(key="snooze_1",   sec="input",  id=1,  name="Snooze Sensor 1",   pf="sw", flag="e,conf,dnm",  rpath="input[idx=0]",   spath="input[id=1].status",  fmt="s",  unit="",  opt={}),
    DP(key="snooze_2",   sec="input",  id=2,  name="Snooze Sensor 2",   pf="sw", flag="e,conf,dnm",  rpath="input[idx=1]",   spath="input[id=2].status",  fmt="s",  unit="",  opt={}),
    DP(key="snooze_3",   sec="input",  id=3,  name="Snooze Sensor 3",   pf="sw", flag="e,conf,dnm",  rpath="input[idx=2]",   spath="input[id=3].status",  fmt="s",  unit="",  opt={}),
    DP(key="snooze_4",   sec="input",  id=4,  name="Snooze Sensor 4",   pf="sw", flag="e,conf,dnm",  rpath="input[idx=3]",   spath="input[id=4].status",  fmt="s",  unit="",  opt={}),
    DP(key="snooze_5",   sec="input",  id=5,  name="Snooze Sensor 5",   pf="sw", flag="e,conf,dnm",  rpath="input[idx=4]",   spath="input[id=5].status",  fmt="s",  unit="",  opt={}),
    DP(key="snooze_6",   sec="input",  id=6,  name="Snooze Sensor 6",   pf="sw", flag="e,conf,dnm",  rpath="input[idx=5]",   spath="input[id=6].status",  fmt="s",  unit="",  opt={}),
    DP(key="snooze_7",   sec="input",  id=7,  name="Snooze Sensor 7",   pf="sw", flag="e,conf,dnm",  rpath="input[idx=6]",   spath="input[id=7].status",  fmt="s",  unit="",  opt={}),
    DP(key="snooze_8",   sec="input",  id=8,  name="Snooze Sensor 8",   pf="sw", flag="e,conf,dnm",  rpath="input[idx=7]",   spath="input[id=8].status",  fmt="s",  unit="",  opt={}),
    DP(key="snooze_9",   sec="input",  id=9,  name="Snooze Sensor 9",   pf="sw", flag="e,conf,dnm",  rpath="input[idx=8]",   spath="input[id=9].status",  fmt="s",  unit="",  opt={}),
    DP(key="snooze_10",  sec="input",  id=10, name="Snooze Sensor 10",  pf="sw", flag="e,conf,dnm",  rpath="input[idx=9]",   spath="input[id=10].status", fmt="s",  unit="",  opt={}),
    DP(key="snooze_11",  sec="input",  id=11, name="Snooze Sensor 11",  pf="sw", flag="e,conf,dnm",  rpath="input[idx=10]",  spath="input[id=11].status", fmt="s",  unit="",  opt={}),
    DP(key="snooze_12",  sec="input",  id=12, name="Snooze Sensor 12",  pf="sw", flag="e,conf,dnm",  rpath="input[idx=11]",  spath="input[id=12].status", fmt="s",  unit="",  opt={}),
    DP(key="snooze_13",  sec="input",  id=13, name="Snooze Sensor 13",  pf="sw", flag="e,conf,dnm",  rpath="input[idx=12]",  spath="input[id=13].status", fmt="s",  unit="",  opt={}),
    DP(key="snooze_14",  sec="input",  id=14, name="Snooze Sensor 14",  pf="sw", flag="e,conf,dnm",  rpath="input[idx=13]",  spath="input[id=14].status", fmt="s",  unit="",  opt={}),
    DP(key="snooze_15",  sec="input",  id=15, name="Snooze Sensor 15",  pf="sw", flag="e,conf,dnm",  rpath="input[idx=14]",  spath="input[id=15].status", fmt="s",  unit="",  opt={}),
    DP(key="snooze_16",  sec="input",  id=16, name="Snooze Sensor 16",  pf="sw", flag="e,conf,dnm",  rpath="input[idx=15]",  spath="input[id=16].status", fmt="s",  unit="",  opt={}),

    DP(key="control_1",  sec="output", id=1,  name="Control 1",  pf="sw",  flag="e,none",  rpath="output[idx=0]",  spath="output[id=1].status",  fmt="s",  unit="",  opt={}),
    DP(key="control_2",  sec="output", id=2,  name="Control 2",  pf="sw",  flag="e,none",  rpath="output[idx=1]",  spath="output[id=2].status",  fmt="s",  unit="",  opt={}),
    DP(key="control_3",  sec="output", id=3,  name="Control 3",  pf="sw",  flag="e,none",  rpath="output[idx=2]",  spath="output[id=3].status",  fmt="s",  unit="",  opt={}),
    DP(key="control_4",  sec="output", id=4,  name="Control 4",  pf="sw",  flag="e,none",  rpath="output[idx=3]",  spath="output[id=4].status",  fmt="s",  unit="",  opt={}),
    DP(key="control_5",  sec="output", id=5,  name="Control 5",  pf="sw",  flag="e,none",  rpath="output[idx=4]",  spath="output[id=5].status",  fmt="s",  unit="",  opt={}),
    DP(key="control_6",  sec="output", id=6,  name="Control 6",  pf="sw",  flag="e,none",  rpath="output[idx=5]",  spath="output[id=6].status",  fmt="s",  unit="",  opt={}),
    DP(key="control_7",  sec="output", id=7,  name="Control 7",  pf="sw",  flag="e,none",  rpath="output[idx=6]",  spath="output[id=7].status",  fmt="s",  unit="",  opt={}),
    DP(key="control_8",  sec="output", id=8,  name="Control 8",  pf="sw",  flag="e,none",  rpath="output[idx=7]",  spath="output[id=8].status",  fmt="s",  unit="",  opt={}),
    DP(key="control_9",  sec="output", id=9,  name="Control 9",  pf="sw",  flag="e,none",  rpath="output[idx=8]",  spath="output[id=9].status",  fmt="s",  unit="",  opt={}),
    DP(key="control_10", sec="output", id=10, name="Control 10", pf="sw",  flag="e,none",  rpath="output[idx=9]",  spath="output[id=10].status", fmt="s",  unit="",  opt={}),
    DP(key="control_11", sec="output", id=11, name="Control 11", pf="sw",  flag="e,none",  rpath="output[idx=10]", spath="output[id=11].status", fmt="s",  unit="",  opt={}),
    DP(key="control_12", sec="output", id=12, name="Control 12", pf="sw",  flag="e,none",  rpath="output[idx=11]", spath="output[id=12].status", fmt="s",  unit="",  opt={}),
    DP(key="control_13", sec="output", id=13, name="Control 13", pf="sw",  flag="e,none",  rpath="output[idx=12]", spath="output[id=13].status", fmt="s",  unit="",  opt={}),
    DP(key="control_14", sec="output", id=14, name="Control 14", pf="sw",  flag="e,none",  rpath="output[idx=13]", spath="output[id=14].status", fmt="s",  unit="",  opt={}),
    DP(key="control_15", sec="output", id=15, name="Control 15", pf="sw",  flag="e,none",  rpath="output[idx=14]", spath="output[id=15].status", fmt="s",  unit="",  opt={}),
    DP(key="control_16", sec="output", id=16, name="Control 16", pf="sw",  flag="e,none",  rpath="output[idx=15]", spath="output[id=16].status", fmt="s",  unit="",  opt={}),

    # All definitions below use BinarySensorDeviceClass.PROBLEM. I.e.False -> OK and True -> Fault
    DP(key="keypad",     sec="keypad", id=0,  name="Keypad",         pf="bin", flag="e,diag",  rpath="=keypad", spath="#keypad",                        fmt="b",  unit="",  opt={}),
    DP(key="system",     sec="system", id=0,  name="System",         pf="bin", flag="e,diag",  rpath="=system", spath="#system",                        fmt="s",  unit="",  opt={}),

    DP(key="mains",      sec="tamper", id=0,  name="Mains Power",    pf="bin", flag="e,diag",  rpath="=tamper", spath="'mains fail' in tamper.status",  fmt="s",  unit="",  opt={}),
    DP(key="battery",    sec="tamper", id=0,  name="Backup Battery", pf="bin", flag="e,diag",  rpath="=tamper", spath="'battery low' in tamper.status", fmt="s",  unit="",  opt={}),
]

DATAPATHS_EXTRA = {
    '#keypad': "$not(is_keypad_bus_online)",
    '#system': "$count(system.status)!=0 or $count(tamper.status)!=0"
}
DATAPATHS_CONST = {
    '=tamper':      { 'name': '', 'icon_name': '', 'is_hidden': False, 'is_active': True},
    '=system':      { 'name': '', 'icon_name': '', 'is_hidden': False, 'is_active': True},
    '=keypad':      { 'name': '', 'icon_name': '', 'is_hidden': False, 'is_active': True},
}

class EliteCloudDatapoint(DP):
    def __init__(self, dp: DP):
        """
        Create a new EliteCloudDatapoint instance
        """
        super().__init__(**asdict(dp))

        # Resolve paths if needed
        if self.rpath.startswith('#'):
            self.rpath = DATAPATHS_EXTRA.get(self.rpath)

        if self.spath.startswith('#'):
            self.spath = DATAPATHS_EXTRA.get(self.spath)
        
        # Resolve flags
        flag_parts = self.flag.split(',')
        self.flag_enabled  = flag_parts[0] if len(flag_parts) > 0 else ''
        self.flag_category = flag_parts[1] if len(flag_parts) > 1 else ''
        self.flag_def_name = flag_parts[2] if len(flag_parts) > 2 else ''


    @staticmethod
    def for_platform(target_platform: str) -> list['EliteCloudDatapoint']:
        """
        Get all datapoints matching the target platform
        """
        pf:str = PLATFORM_TO_PF.get(target_platform, None)
        if pf is None:
            _LOGGER.warning(f"Trying to get abbreviated platform for '{target_platform}. Please contact the developer of this integration.")
            return []

        # Collect all datapoints associated with this device family and for this platform 
        return [ EliteCloudDatapoint(dp) for dp in DATAPOINTS if dp.pf==pf  ]


    @staticmethod
    def for_all() -> list['EliteCloudDatapoint']:
        return [ EliteCloudDatapoint(dp) for dp in DATAPOINTS ]
    

@dataclass
class EliteCloudDeviceConfig():

    uuid: str
    name: str
    serial: str
    mac: str
    type: str
    pnl_version: str
    mod_version: str
    resources: 'list[EliteCloudDeviceResource]'


    @staticmethod
    def from_data(d: dict[str,Any]):
        """
        """
        return EliteCloudDeviceConfig(
            uuid        = d.get("uuid", None),
            name        = d.get("name", None),
            serial      = d.get("panel", {}).get("serial_no", None),
            mac         = d.get("panel", {}).get("mac_address", None),
            type        = d.get("panel", {}).get("specification", {}).get("module_type", None),
            pnl_version = d.get("panel", {}).get("specification", {}).get("panel_version", None),
            mod_version = d.get("panel", {}).get("specification", {}).get("module_version", None),
            resources   = EliteCloudDeviceResource.from_data(d.get("resources", {}))
        )
    

    @staticmethod
    def from_dict(d: dict[str,Any]) -> 'EliteCloudDeviceConfig':        
        """
        Construct a new EliteCloudDeviceConfig object from a dict
        """
        return EliteCloudDeviceConfig(
            uuid        = d.get("uuid", None),
            name        = d.get("name", None),
            serial      = d.get("serial", None),
            mac         = d.get("mac", None),
            type        = d.get("type", None),
            pnl_version = d.get("pnl_version"),
            mod_version = d.get("mod_version"),
            resources   = EliteCloudDeviceResource.from_list(d.get("resources", {})),
        )


@dataclass
class EliteCloudDeviceResource():

    key: str
    name: str
    icon: str
    is_hidden: bool
    is_active: bool

        
    @staticmethod
    def from_data(d: dict[str,Any]) -> 'list[EliteCloudDeviceResource]':
        """
        get struct that defines properties for this datapoint
        """
        result: list[EliteCloudDeviceResource] = []
        
        for datapoint in EliteCloudDatapoint.for_all():
            try:
                if datapoint.rpath.startswith('='):
                    # Predefined constant result
                    r = DATAPATHS_CONST.get(datapoint.rpath)
                else:
                    # Lookup the resource struct for this datapoint
                    r = Jsonata(datapoint.rpath).evaluate(d)
                
                if not isinstance(r, dict):
                    continue

                name = r.get("name")
                if not name or datapoint.flag_def_name:
                    name = datapoint.name

                res = EliteCloudDeviceResource(
                    key = datapoint.key,
                    name = name,
                    icon = r.get("icon_name"),
                    is_hidden = r.get("is_hidden", True),
                    is_active = r.get("is_active", False),
                )
                result.append(res)
            
            except Exception as ex:
                _LOGGER.debug(f"Could not resolve path {datapoint.rpath} for {datapoint.key}: {str(ex)}")

        return result


    @staticmethod
    def from_list(l: list[Any]) -> 'list[EliteCloudDeviceResource]':
        """
        """
        result: list[EliteCloudDeviceResource] = []
        for r in l:
            res = EliteCloudDeviceResource(
                key = r.get('key'),
                name = r.get("name"),
                icon = r.get('icon'),
                is_hidden = r.get("is_hidden", True),
                is_active = r.get("is_active", False),
            )
            result.append(res)

        return result


@dataclass
class EliteCloudDeviceStatus():

    uuid: str
    _statuses: dict[str,str]

    def get(self, key: str, default=None) -> str:
        return self._statuses.get(key, default)


    @staticmethod
    def from_data(uuid:str, d: dict[str,Any]) -> 'EliteCloudDeviceStatus':
        """
        get struct that defines properties for this datapoint
        """
        statuses: dict[str,str] = {}
        
        for datapoint in EliteCloudDatapoint.for_all():
            try:
                if datapoint.spath.startswith('='):
                    # Predefined constant result
                    val = DATAPATHS_CONST.get(datapoint.spath)
                else:
                    # Lookup the resource struct for this datapoint
                    val = Jsonata(datapoint.spath).evaluate(d)
                
                # Some EliteCloud values are returned as array; i.e. input[idx=1].status == ['open']
                if isinstance(val, list):
                    val = str.join(',', [str(i) for i in val if i is not None])
                else:
                    val = str(val)

                statuses[datapoint.key] = val
            
            except Exception as ex:
                _LOGGER.debug(f"Could not resolve path {datapoint.spath} for {datapoint.key}: {str(ex)}")

        return EliteCloudDeviceStatus(
            uuid = uuid,
            _statuses = statuses
        )

