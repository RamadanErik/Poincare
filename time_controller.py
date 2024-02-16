import sys
import logging


'------------Detektor importok-------------------'

sys.path.append("C:\\Users\\KNL2022\\Documents\\TimeController_V1_10_0\\Examples\\Python")
from utils.common import connect, assert_arg_range
from utils.acquisitions import (
    setup_input_counts_over_time_acquisition,
    acquire_counts_over_time,
    save_counts_over_time,
    COUNT_OVER_TIME_INPUTS,
)
from utils.common import zmq_exec, trim_unit
#from utils.plot import plot_histograms
#from utils.consts import HIST_BCOU_RANGE, HIST_BWID_RANGE

logger = logging.getLogger(__name__)
'------------Time controller beállítása---------------------'
# Default Time Controller IP address
DEFAULT_TC_ADDRESS = "169.254.104.112"
# Default number of counter acquisitions
DEFAULT_NUMBER_OF_ACQUISITIONS = 5
# Default file path where counts are saved in CSV format (None = do not save)
DEFAULT_COUNTS_FILEPATH = "input_counts.csv"
# Default counter integration time ps
mp=1 #Másodpercben az integration time
DEFAULT_COUNTERS_INTEGRATION_TIME = int(mp*(10^12))
# Default list of input counts to acquire
DEFAULT_COUNTERS = ["1", "2", "3", "4"]
# Default log file path where logging output is stored
DEFAULT_LOG_PATH = None
'------------------------------------------------------------'

def time_controller_csatlakozas():
    try:
        # Default Time Controller IP address
        DEFAULT_TC_ADDRESS = "169.254.104.112"

        # Default number of counter acquisitions
        DEFAULT_NUMBER_OF_ACQUISITIONS = 5

        # Default file path where counts are saved in CSV format (None = do not save)
        DEFAULT_COUNTS_FILEPATH = "input_counts.csv"

        # Default counter integration time ps
        mp = 1  # Másodpercben az integration time
        DEFAULT_COUNTERS_INTEGRATION_TIME = int(mp * (10 ^ 12))

        # Default list of input counts to acquire
        DEFAULT_COUNTERS = ["1", "2", "3", "4"]

        # Default log file path where logging output is stored
        DEFAULT_LOG_PATH = None

        tc = connect(DEFAULT_TC_ADDRESS)
        hist_to_counter_map, actual_integration_time = setup_input_counts_over_time_acquisition(
            tc, DEFAULT_COUNTERS_INTEGRATION_TIME, DEFAULT_COUNTERS
        )
    except AssertionError as e:
        logger.error(e)
        sys.exit(1)

    except ConnectionError as e:
        logger.exception(e)
        sys.exit(1)
    return tc
