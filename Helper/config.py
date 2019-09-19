import yaml
from os.path import exists, abspath
from shutil import copy
from typing import Dict, List, Tuple, Optional
import logging
from os.path import realpath, join
import platform
from .log_level import Level


class validable:
    def __init__(self, data: Dict, section: str,
                 defaults: Dict[str, Tuple[Optional[object], "Level"]]):
        self.data = data
        self.section = section
        self.defaults = defaults

    def _keyOrDefault(self, key: str):
        if key in self.data.keys():
            return self.data[key]
        else:
            default = self.defaults.get(key, None)
            return default[0] if default is not None else None

    @property
    def Validation(self) -> List[Tuple['Level', str]]:
        res = []
        for key in self.defaults.keys():
            if key not in self.data:
                default, level = self.defaults[key]
                defaultText = f", using default '{default}'" if default is not None else ""
                res.append((level, f"'{key}' not defined under '{self.section}'{defaultText}"))
        if len(res) == 0:
            values = '; '.join([f'{key}: {self.data[key]}' for key in self.defaults.keys()])
            res.append((Level.INFO, f'{self.section} [{values}]'))
        return res


class restApi(validable):
    def __init__(self, data: Dict, section: str, defaults: Dict[str, Tuple[Optional[object], "Level"]]):
        if 'Host' not in defaults.keys(): defaults['Host'] = (None, Level.ERROR)
        if 'Port' not in defaults.keys(): defaults['Port'] = (None, Level.ERROR)
        super().__init__(data, section, defaults)

    @property
    def Host(self):
        return self._keyOrDefault('Host')

    @property
    def Port(self):
        return self._keyOrDefault('Port')


class Grafana(restApi):
    def __init__(self, data: Dict):
        defaults = {
            'Enabled': (False, Level.WARNING),
            'Bearer': ('', Level.WARNING),
            'ReportGenerator': ('', Level.WARNING)
        }
        super().__init__(data, "Grafana", defaults)

    @property
    def Enabled(self):
        return self._keyOrDefault('Enabled')

    @property
    def Bearer(self):
        return self._keyOrDefault('Bearer')

    @property
    def ReportGenerator(self):
        return self._keyOrDefault('ReportGenerator')

    @property
    def Validation(self) -> List[Tuple['Level', str]]:
        if not self.Enabled:
            return [(Level.INFO, "Grafana is disabled")]
        else:
            return super().Validation


class TapConfig(validable):
    def __init__(self, data: Dict):
        defaults = {
            'Enabled': (False, Level.WARNING),
            'Exe': ('Keysight.Tap.Cli.exe', Level.WARNING),
            'Folder': ('C:/Program Files/Keysight/TAP8', Level.WARNING),
            'Results': ('C:/Program Files/Keysight/TAP8/Results', Level.WARNING),
            'EnsureClosed': (False, Level.WARNING),
        }
        super().__init__(data, 'Tap', defaults)

    @property
    def Enabled(self):
        return self._keyOrDefault('Enabled')

    @property
    def Exe(self):
        return self._keyOrDefault('Exe')

    @property
    def Folder(self):
        return self._keyOrDefault('Folder')

    @property
    def Results(self):
        return self._keyOrDefault('Results')

    @property
    def EnsureClosed(self):
        return self._keyOrDefault('EnsureClosed')

    @property
    def Path(self): return realpath(join(self.Folder, self.Exe))

    @property
    def Validation(self) -> List[Tuple['Level', str]]:
        if not self.Enabled:
            if 'Enabled' in self.data.keys():
                return [(Level.INFO, "TAP is disabled")]
            else:
                return [(Level.ERROR, "'Enabled' key not in 'Tap' configuration. Assuming Disabled.")]
        else:
            return super().Validation


class Dispatcher(restApi):
    def __init__(self, data: Dict):
        super().__init__(data, 'Dispatcher', {})


class SliceManager(restApi):
    def __init__(self, data: Dict):
        super().__init__(data, 'SliceManager', {})


class InfluxDb(restApi):
    def __init__(self, data: Dict):
        defaults = {
            'Enabled': (False, Level.WARNING),
            'User': (None, Level.ERROR),
            'Password': (None, Level.ERROR),
            'Database': (None, Level.ERROR),
        }
        super().__init__(data, 'InfluxDb', defaults)

    @property
    def Enabled(self):
        return self._keyOrDefault('Enabled')

    @property
    def User(self):
        return self._keyOrDefault('User')

    @property
    def Password(self):
        return self._keyOrDefault('Password')

    @property
    def Database(self):
        return self._keyOrDefault('Database')

    @property
    def Validation(self) -> List[Tuple['Level', str]]:
        if not self.Enabled:
            if 'Enabled' in self.data.keys():
                return [(Level.INFO, "InfluxDb is disabled")]
            else:
                return [(Level.ERROR, "'Enabled' key not in 'InfluxDb' configuration. Assuming Disabled.")]
        else:
            return super().Validation


class Logging(validable):
    def __init__(self, data: Dict):
        defaults = {
            'Folder': ('Logs', Level.WARNING),
            'AppLevel': ('info', Level.WARNING),
            'LogLevel': ('debug', Level.WARNING)
        }
        super().__init__(data, 'Logging', defaults)

    @staticmethod
    def toLogLevel(level: Optional[str]) -> int:
        if level is None or level.lower() == 'debug': return logging.DEBUG
        if level.lower() == 'info': return logging.INFO
        if level.lower() == 'warning': return logging.WARNING
        if level.lower() == 'error': return logging.ERROR
        return logging.CRITICAL

    @property
    def Folder(self):
        folder = self._keyOrDefault("Folder")
        return abspath(folder)

    @property
    def AppLevel(self):
        return self.toLogLevel(self._keyOrDefault("AppLevel"))

    @property
    def LogLevel(self):
        return self.toLogLevel(self._keyOrDefault("LogLevel"))


class Metadata(validable):
    def __init__(self, data: Dict):
        defaults = {
            "HostIp": ("127.0.0.1", Level.INFO),
            "Facility": ("", Level.INFO),
        }
        super().__init__(data, 'Metadata', defaults)

        self.HostName = platform.node()

    @property
    def HostIp(self): return self._keyOrDefault("HostIp")

    @property
    def Facility(self): return self._keyOrDefault("Facility")


class Config:
    FILENAME = 'config.yml'

    data = None
    Validation: List[Tuple['Level', str]] = []

    def __init__(self):
        if self.data is None:
            self.Reload()

    def Reload(self):
        if not exists(self.FILENAME):
            copy('Helper/default_config', self.FILENAME)

        try:
            with open(self.FILENAME, 'r', encoding='utf-8') as file:
                self.data = yaml.safe_load(file)
        except Exception as e:
            from .log import Log
            Log.C(f"Exception while loading config file: {e}")
            return

        self.Validate()

    @property
    def Logging(self):
        return Logging(self.data.get('Logging', {}))

    @property
    def Dispatcher(self):
        return Dispatcher(self.data.get('Dispatcher', {}))

    @property
    def Flask(self):
        return self.data['Flask']

    @property
    def TempFolder(self):
        return self.data.get('TempFolder', 'Temp')

    @property
    def Tap(self):
        return TapConfig(self.data.get('Tap', {}))

    @property
    def Grafana(self):
        return Grafana(self.data.get('Grafana', {}))

    @property
    def SliceManager(self):
        return SliceManager(self.data.get('SliceManager', {}))

    @property
    def InfluxDb(self):
        return InfluxDb(self.data.get('InfluxDb', {}))

    @property
    def Metadata(self):
        return Metadata(self.data.get('Metadata', {}))

    def Validate(self):
        self.Validation = []
        if 'Flask' not in self.data or 'SECRET_KEY' not in self.Flask:
            self.Validation.append((Level.ERROR, "Secret key not defined ('Flask: SECRET_KEY: <value>')"))
        if 'TempFolder' not in self.data:
            self.Validation.append((Level.INFO, "TempFolder not defined, using 'Temp'"))

        for entry in [self.Logging, self.Dispatcher, self.SliceManager, self.Tap,
                      self.Grafana, self.InfluxDb, self.Metadata, ]:
            self.Validation.extend(entry.Validation)
