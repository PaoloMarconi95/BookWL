from Config.Configuration import Configuration
from Config.Logger import Logger
from Config.FutureBookingConfiguration import FutureBookingConfiguration

CONFIG: Configuration = Configuration()
CONFIG.load()

FUTUREBOOKINGCONFIG: FutureBookingConfiguration = FutureBookingConfiguration()
FUTUREBOOKINGCONFIG.load()

LOGGER: Logger = Logger()
