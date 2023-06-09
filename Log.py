import datetime as dt
from datetime import datetime
import os
import pathlib

class Log:
    def __init__(self):
        # initialize a log file, named after the date in which it was created
        folder = self.__initialize_log_directory()
        self.file = open(os.path.join(folder, (str(dt.date.today()) + '.txt')), 'w+')
        self.file.close()
        super().__init__()
        Log.instance = self

    def __initialize_log_directory(self):
        log_folder = os.path.join(pathlib.Path(__file__).parent.resolve(), 'Logs')
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)
        return log_folder

    def info(self, msg):
        self.__write(msg, 'info')

    def warn(self, msg):
        self.__write(msg, 'warn')

    def error(self, msg):
        self.__write(msg, 'error')

    def __write(self, msg, severity):
        print(str(datetime.now().time()) + ' - ' + severity.upper() + ": " + msg)
        self.file = open(self.file.name, 'a')
        self.file.write(str(datetime.now().time()) + ' - ' + severity.upper() + ": " + msg + '\n')
        self.file.close()

logger = Log()