import subprocess
from Helper import Level
from typing import Callable, List


class Cli:
    def __init__(self, parameters: List[str], cwd: str, logger: Callable):

        aux_list = list(map(str.split, parameters))
        self.parameters = [elem for sublist in aux_list for elem in sublist]
        self.cwd = cwd
        self.logger = logger

    def Execute(self) -> int:
        process = subprocess.Popen(self.parameters, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, cwd=self.cwd)
        self.stdout(process)
        return process.wait()

    def stdout(self, process: subprocess.Popen):
        pipe = process.stdout

        for line in iter(pipe.readline, b''):
            try:
                line = line.decode('utf-8').rstrip()
            except Exception as e:
                line = f"DECODING EXCEPTION: {e}"

            self.logger(Level.INFO, f"[CLI]{line}")
