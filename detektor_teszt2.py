import argparse
import logging

from pathlib import Path

import csv

import time
import clr
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime

matplotlib.use('TkAgg')
import sys

idokezdet = datetime.datetime.now()


'----------------KINESIS importok--------------'
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.PolarizerCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.PolarizerCLI import *
from System import Decimal

'---------------------------------------------------'



'ötletek'
###intergrációs idő kalibrálás az elején
###optimum elmentése fileba
###hirtelen dropnál jelezzen amikor élesben megy
'----'

'------------Detektor importok-------------------'

sys.path.append("C:\\Users\\KNL2022\\Documents\\TimeController_V1_10_0\\Examples\\Python")
from utils.common import connect, assert_arg_range
from utils.acquisitions import (
    setup_input_counts_over_time_acquisition,
    acquire_counts_over_time,
    save_counts_over_time,
    COUNT_OVER_TIME_INPUTS,
)
from utils.common import zmq_exec
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
mp=0.5 #Másododpercben az integration time
DEFAULT_COUNTERS_INTEGRATION_TIME = int(mp*(10^12))
# Default list of input counts to acquire
DEFAULT_COUNTERS = ["1", "2", "3", "4"]
# Default log file path where logging output is stored
DEFAULT_LOG_PATH = None
'------------------------------------------------------------'


"""------------------FÜGGVÉNYEK-----------------------"""
from fuggvenyek import *
"""---------------------------------------------------"""

def main():
    for i in range(3):
        device,paddle1,paddle2,paddle3=kontrollerhez_csatlakozas()
        tc=time_controller_csatlakozas()

        fokok, adatok3, optimum=kereso_algoritmus_sima(device,tc,2,10)
        opt_mert=[]
        for j in range(1, 5):
            adat2 = zmq_exec(tc, f"INPUt{j}:COUNter?")
            adat = int(adat2)
            opt_mert.append(adat)



        save_counts_to_csv(fokok,adatok3,optimum,opt_mert)
        #plt.show()
    sys.exit(0)


if __name__ == "__main__":
    main()
