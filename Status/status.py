from Experiment import Experiment
from .experiment_queue import ExperimentQueue
from threading import Lock
from Helper import Serialize
from os.path import exists, dirname
from os import makedirs


def synchronized(lock):
    def wrap(f):
        def new_funct(*args, **kwargs):
            lock.acquire()
            try:
                return f(*args, **kwargs)
            finally:
                lock.release()
        return new_funct
    return wrap


class Status:
    FILENAME = 'persistence.yml'

    lock = Lock()
    nextId = 0

    _persistence_yml = {'NextId': 0}

    @classmethod
    @synchronized(lock)
    def Initialize(cls):
        path = Serialize.Path('persistence.yml')

        if not exists(path):
            makedirs(dirname(path), exist_ok=True)
            Serialize.Save(cls._persistence_yml, path)

        data = Serialize.Load(path)
        cls.nextId = data['NextId']

    @classmethod
    @synchronized(lock)
    def Save(cls):
        data = {'NextId': cls.nextId}
        Serialize.Save(data, Serialize.Path('persistence.yml'))

    @classmethod
    def NextId(cls):
        res = cls.nextId
        cls.nextId += 1
        cls.Save()
        return res

    @classmethod
    def CreateExperiment(cls) -> (int, Experiment):
        experimentId = cls.NextId()
        experiment = ExperimentQueue.Create(experimentId)
        return experimentId, experiment

    @classmethod
    def DeleteExperiment(cls, experimentId: int):
        ExperimentQueue.Delete(experimentId)

    @classmethod
    def CancelExperiment(cls, experimentId: int):
        ExperimentQueue.Cancel(experimentId)
