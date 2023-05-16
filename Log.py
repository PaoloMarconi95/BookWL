import datetime as dt
from datetime import datetime

class Log:
    def __init__(self):
        # initialize a log file, named after the date in which it was created
        self.file = open('./Logs/' + str(dt.date.today()) + '_' + 'BookWL' + '.txt', 'w+')
        self.file.close()
        super().__init__()
        Log.instance = self

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