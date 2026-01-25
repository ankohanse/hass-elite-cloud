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
    pf: str             # Target platform abbreviation; Sensor, Binary_Sensor etc. If None then not added as entity but may be used internally
    flag: str           # Comma separated flags: enabled/disabled (e or d), entity category (conf, diag or none) 
    rpath: str          # Path for resource params within responses from remote server
    spath: str          # Path for status value within responses from remote server. Note the offset between idx and id!
    fmt: type           # Data format (s=str, b=bool, i=int, t=timestamp, f[n]=float with precision)
    unit: str           # Data unit of measurement
    opt: dict[str,Any]  # Options for Enums

DATAPOINTS = [
    DP(key="area_0",    pf="bin",  flag="e,none",  rpath="area[idx=0]",    spath="area[id=1].status",   fmt="b",  unit="",  opt={}),
    DP(key="area_1",    pf="bin",  flag="e,none",  rpath="area[idx=1]",    spath="area[id=2].status",   fmt="b",  unit="",  opt={}),
    DP(key="area_2",    pf="bin",  flag="e,none",  rpath="area[idx=2]",    spath="area[id=3].status",   fmt="b",  unit="",  opt={}),
    DP(key="area_3",    pf="bin",  flag="e,none",  rpath="area[idx=3]",    spath="area[id=4].status",   fmt="b",  unit="",  opt={}),
    DP(key="area_4",    pf="bin",  flag="e,none",  rpath="area[idx=4]",    spath="area[id=5].status",   fmt="b",  unit="",  opt={}),
    DP(key="area_5",    pf="bin",  flag="e,none",  rpath="area[idx=5]",    spath="area[id=6].status",   fmt="b",  unit="",  opt={}),
    DP(key="area_6",    pf="bin",  flag="e,none",  rpath="area[idx=6]",    spath="area[id=7].status",   fmt="b",  unit="",  opt={}),
    DP(key="area_7",    pf="bin",  flag="e,none",  rpath="area[idx=7]",    spath="area[id=8].status",   fmt="b",  unit="",  opt={}),
    DP(key="area_8",    pf="bin",  flag="e,none",  rpath="area[idx=8]",    spath="area[id=9].status",   fmt="b",  unit="",  opt={}),
    DP(key="area_9",    pf="bin",  flag="e,none",  rpath="area[idx=9]",    spath="area[id=10].status",  fmt="b",  unit="",  opt={}),
    DP(key="area_10",   pf="bin",  flag="e,none",  rpath="area[idx=10]",   spath="area[id=11].status",  fmt="b",  unit="",  opt={}),
    DP(key="area_11",   pf="bin",  flag="e,none",  rpath="area[idx=11]",   spath="area[id=12].status",  fmt="b",  unit="",  opt={}),
    DP(key="area_12",   pf="bin",  flag="e,none",  rpath="area[idx=12]",   spath="area[id=13].status",  fmt="b",  unit="",  opt={}),
    DP(key="area_13",   pf="bin",  flag="e,none",  rpath="area[idx=13]",   spath="area[id=14].status",  fmt="b",  unit="",  opt={}),
    DP(key="area_14",   pf="bin",  flag="e,none",  rpath="area[idx=14]",   spath="area[id=15].status",  fmt="b",  unit="",  opt={}),
    DP(key="area_15",   pf="bin",  flag="e,none",  rpath="area[idx=15]",   spath="area[id=16].status",  fmt="b",  unit="",  opt={}),

    DP(key="input_0",   pf="bin",  flag="e,none",  rpath="input[idx=0]",   spath="input[id=1].status",  fmt="b",  unit="",  opt={}),
    DP(key="input_1",   pf="bin",  flag="e,none",  rpath="input[idx=1]",   spath="input[id=2].status",  fmt="b",  unit="",  opt={}),
    DP(key="input_2",   pf="bin",  flag="e,none",  rpath="input[idx=2]",   spath="input[id=3].status",  fmt="b",  unit="",  opt={}),
    DP(key="input_3",   pf="bin",  flag="e,none",  rpath="input[idx=3]",   spath="input[id=4].status",  fmt="b",  unit="",  opt={}),
    DP(key="input_4",   pf="bin",  flag="e,none",  rpath="input[idx=4]",   spath="input[id=5].status",  fmt="b",  unit="",  opt={}),
    DP(key="input_5",   pf="bin",  flag="e,none",  rpath="input[idx=5]",   spath="input[id=6].status",  fmt="b",  unit="",  opt={}),
    DP(key="input_6",   pf="bin",  flag="e,none",  rpath="input[idx=6]",   spath="input[id=7].status",  fmt="b",  unit="",  opt={}),
    DP(key="input_7",   pf="bin",  flag="e,none",  rpath="input[idx=7]",   spath="input[id=8].status",  fmt="b",  unit="",  opt={}),
    DP(key="input_8",   pf="bin",  flag="e,none",  rpath="input[idx=8]",   spath="input[id=9].status",  fmt="b",  unit="",  opt={}),
    DP(key="input_9",   pf="bin",  flag="e,none",  rpath="input[idx=9]",   spath="input[id=10].status", fmt="b",  unit="",  opt={}),
    DP(key="input_10",  pf="bin",  flag="e,none",  rpath="input[idx=10]",  spath="input[id=11].status", fmt="b",  unit="",  opt={}),
    DP(key="input_11",  pf="bin",  flag="e,none",  rpath="input[idx=11]",  spath="input[id=12].status", fmt="b",  unit="",  opt={}),
    DP(key="input_12",  pf="bin",  flag="e,none",  rpath="input[idx=12]",  spath="input[id=13].status", fmt="b",  unit="",  opt={}),
    DP(key="input_13",  pf="bin",  flag="e,none",  rpath="input[idx=13]",  spath="input[id=14].status", fmt="b",  unit="",  opt={}),
    DP(key="input_14",  pf="bin",  flag="e,none",  rpath="input[idx=14]",  spath="input[id=15].status", fmt="b",  unit="",  opt={}),
    DP(key="input_15",  pf="bin",  flag="e,none",  rpath="input[idx=15]",  spath="input[id=16].status", fmt="b",  unit="",  opt={}),

    DP(key="output_0",  pf="bin",  flag="e,none",  rpath="output[idx=0]",  spath="output[id=1].status",  fmt="b",  unit="",  opt={}),
    DP(key="output_1",  pf="bin",  flag="e,none",  rpath="output[idx=1]",  spath="output[id=2].status",  fmt="b",  unit="",  opt={}),
    DP(key="output_2",  pf="bin",  flag="e,none",  rpath="output[idx=2]",  spath="output[id=3].status",  fmt="b",  unit="",  opt={}),
    DP(key="output_3",  pf="bin",  flag="e,none",  rpath="output[idx=3]",  spath="output[id=4].status",  fmt="b",  unit="",  opt={}),
    DP(key="output_4",  pf="bin",  flag="e,none",  rpath="output[idx=4]",  spath="output[id=5].status",  fmt="b",  unit="",  opt={}),
    DP(key="output_5",  pf="bin",  flag="e,none",  rpath="output[idx=5]",  spath="output[id=6].status",  fmt="b",  unit="",  opt={}),
    DP(key="output_6",  pf="bin",  flag="e,none",  rpath="output[idx=6]",  spath="output[id=7].status",  fmt="b",  unit="",  opt={}),
    DP(key="output_7",  pf="bin",  flag="e,none",  rpath="output[idx=7]",  spath="output[id=8].status",  fmt="b",  unit="",  opt={}),
    DP(key="output_8",  pf="bin",  flag="e,none",  rpath="output[idx=8]",  spath="output[id=9].status",  fmt="b",  unit="",  opt={}),
    DP(key="output_9",  pf="bin",  flag="e,none",  rpath="output[idx=9]",  spath="output[id=10].status", fmt="b",  unit="",  opt={}),
    DP(key="output_10", pf="bin",  flag="e,none",  rpath="output[idx=10]", spath="output[id=11].status", fmt="b",  unit="",  opt={}),
    DP(key="output_11", pf="bin",  flag="e,none",  rpath="output[idx=11]", spath="output[id=12].status", fmt="b",  unit="",  opt={}),
    DP(key="output_12", pf="bin",  flag="e,none",  rpath="output[idx=12]", spath="output[id=13].status", fmt="b",  unit="",  opt={}),
    DP(key="output_13", pf="bin",  flag="e,none",  rpath="output[idx=13]", spath="output[id=14].status", fmt="b",  unit="",  opt={}),
    DP(key="output_14", pf="bin",  flag="e,none",  rpath="output[idx=14]", spath="output[id=15].status", fmt="b",  unit="",  opt={}),
    DP(key="output_15", pf="bin",  flag="e,none",  rpath="output[idx=15]", spath="output[id=16].status", fmt="b",  unit="",  opt={}),

    DP(key="tamper",    pf="bin",  flag="e,none",  rpath="=tamper",        spath="tamper.status",        fmt="b",  unit="",  opt={}),
    DP(key="system",    pf="bin",  flag="e,none",  rpath="=system",        spath="system.status",        fmt="b",  unit="",  opt={}),
]

DATAPATHS_EXTRA = {
    '#canEdit':     "$lookup(members, context.profile_id).canEdit",
    '#enabled':     "$lookup(members, context.profile_id).enabled",
}
DATAPATHS_CONST = {
    '=tamper':      { 'name': 'tamper', 'icon_name': '', 'is_hidden': False, 'is_active': True},
    '=system':      { 'name': 'system', 'icon_name': '', 'is_hidden': False, 'is_active': True},
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
    version: str
    resources: 'list[EliteCloudDeviceResource]'


    @staticmethod
    def from_data(d: dict[str,Any]):
        """
        """
        return EliteCloudDeviceConfig(
            uuid       = d.get("uuid", None),
            name       = d.get("name", None),
            serial     = d.get("panel", {}).get("serial_no", None),
            mac        = d.get("panel", {}).get("mac_address", None),
            type       = d.get("panel", {}).get("specification", {}).get("module_type", None),
            version    = d.get("panel", {}).get("specification", {}).get("module_version", None),
            resources  = EliteCloudDeviceResource.from_data(d.get("resources", {}))
        )
    

    @staticmethod
    def from_dict(d: dict[str,Any]) -> 'EliteCloudDeviceConfig':        
        """
        Construct a new EliteCloudDeviceConfig object from a dict
        """
        return EliteCloudDeviceConfig(
            uuid       = d.get("uuid", None),
            name       = d.get("name", None),
            serial     = d.get("serial", None),
            mac        = d.get("mac", None),
            type       = d.get("type", None),
            version    = d.get("version", None),
            resources  = EliteCloudDeviceResource.from_list(d.get("resources", {})),
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

                res = EliteCloudDeviceResource(
                    key = datapoint.key,
                    name = r.get("name"),
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

