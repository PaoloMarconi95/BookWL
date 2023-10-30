from Config.Configuration import Configuration
from Config.Logger import Logger

CONFIG: Configuration = Configuration()
CONFIG.load()

LOGGER: Logger = Logger()