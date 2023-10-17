import datetime as dt
import threading
from datetime import datetime
import os
import pathlib


class Log:
    def __init__(self):
        # initialize a log file, named after the date in which it was created
        folder = self.__initialize_log_directory()
        self.file = open(os.path.join(folder, (str(dt.date.today()) + '.log')), 'a')
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
        final_message = f"Thread {threading.get_ident()} - {str(datetime.now().strftime('%d/%m %H:%M:%S'))} - {severity.upper()}: {str(msg)} \n"
        print(final_message, end="")
        self.file = open(self.file.name, 'a')
        self.file.write(final_message)
        self.file.close()


logger = Log()
