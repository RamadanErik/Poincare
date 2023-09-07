import sys
import argparse
import logging
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.common import connect, assert_arg_range
from utils.acquisitions import (
    setup_input_counts_over_time_acquisition,
    acquire_counts_over_time,
    save_counts_over_time,
    COUNT_OVER_TIME_INPUTS,
)
from utils.common import zmq_exec
from utils.plot import plot_histograms
from utils.consts import HIST_BCOU_RANGE, HIST_BWID_RANGE

logger = logging.getLogger(__name__)

"------------------------------------------------------------"

# Default Time Controller IP address
DEFAULT_TC_ADDRESS = "169.254.104.112"

# Default number of counter acquisitions
DEFAULT_NUMBER_OF_ACQUISITIONS = 5

# Default file path where counts are saved in CSV format (None = do not save)
DEFAULT_COUNTS_FILEPATH = "input_counts.csv"

# Default counter integration time ps
DEFAULT_COUNTERS_INTEGRATION_TIME = 1000000000000

# Default list of input counts to acquire
DEFAULT_COUNTERS = ["1", "2", "3", "4"]

# Default log file path where logging output is stored
DEFAULT_LOG_PATH = None


def main():
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
        filename=args.log_path
    )


    try:
        assert len(args.counters) <= 4, "Select at most 4 input channels to acquire"
        assert_arg_range("--acquisitions", args.acquisitions, HIST_BCOU_RANGE)
        assert_arg_range("--integration", args.integration, HIST_BWID_RANGE)

        tc = connect(args.address) #######fontos###
        hist_to_counter_map, actual_integration_time = setup_input_counts_over_time_acquisition(
                tc, args.integration, args.counters
        )
        if actual_integration_time != args.integration:
            logger.warning(
                f"counters integration time adjusted to {actual_integration_time}ps to work with the current resolution"
            )

        logger.info(
            f"acquire {args.acquisitions} individual counts over {args.acquisitions * actual_integration_time} ps"
        )

        "----------------hisztogramhoz-------------------"
        counts = acquire_counts_over_time(
            tc,
            actual_integration_time,
            args.acquisitions,
            hist_to_counter_map,
        )

        if args.counts_filepath: #mentés
            save_counts_over_time(
                counts,
                actual_integration_time,
                args.counts_filepath,
            )

        plot_histograms(
            counts,
            actual_integration_time,
            title="Input counts over time",
        )
        "-------------------------------------------------"

        for i in range(1,5):
            adat=zmq_exec(tc, f"HIST{i}:DATA?") ###fontos####
            adat2=zmq_exec(tc,f"INPUt{i}:COUNter?")   #fontos#
            print(adat)
            print(adat2)

    except AssertionError as e:
        logger.error(e)
        sys.exit(1)

    except ConnectionError as e:
        logger.exception(e)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()