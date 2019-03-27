from .user import User
from Helper import Serialize
from typing import Dict, Tuple, List


class ExperimentDescriptor:
    def __init__(self, data: Dict):
        self.Valid, self.Missing = self.validate(data)
        self._data = data
        if self.Valid:
            self.User = User(self._data['User'])

    @staticmethod
    def validate(data: Dict) -> Tuple[bool, List[str]]:
        keys = ['Id', 'Name', 'Platform', 'TestCases', 'UEs', 'User']
        return Serialize.CheckKeys(data, *keys)

    @property
    def Id(self) -> int:
        return self._data['Id']

    @property
    def Name(self) -> str:
        return self._data['Name']

    @property
    def Platform(self) -> str:
        return self._data['Platform']

    @property
    def TestCases(self) -> List[str]:
        return self._data['TestCases']

    @property
    def UEs(self) -> List[Dict[str, Dict]]:
        return self._data['UEs']
