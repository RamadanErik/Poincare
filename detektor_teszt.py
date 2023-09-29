#import sys
import argparse
import logging
import time
#import iranyitas
from pathlib import Path

import csv
import os
import time
import ctypes
from ctypes import *
import time
import clr
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime

matplotlib.use('TkAgg')
import sys

idokezdet = datetime.datetime.now()



clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.PolarizerCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.PolarizerCLI import *
from System import Decimal




###intergrációs idő kalibrálás az elején
###optimum elmentése fileba
###hirtelen dropnál jelezzen amikor élesben megy




sys.path.append("C:\\Users\\KNL2022\\Documents\\TimeController_V1_10_0\\Examples\\Python")
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
DEFAULT_COUNTERS_INTEGRATION_TIME = 500000000000

# Default list of input counts to acquire
DEFAULT_COUNTERS = ["1", "2", "3", "4"]

# Default log file path where logging output is stored
DEFAULT_LOG_PATH = None



"""------------------FÜGGVÉNYEK-----------------------"""


def save_counts_to_csv(counts, filepath):
    with open(filepath, 'a', newline="") as csvfile:
        writer_object = csv.writer(csvfile, delimiter=";")
        for i in range(4):
            for j in range(len(counts[0])):
                lista=[]
                for k in range(9):
                    lista.append(counts[i][j][k])
                writer_object.writerow(lista)
                print(lista)


        csvfile.close()
    return


def optimum_kereso(device,tc,paddle,min,max,db):
    adatok=[]

    probalk=[]
    adat_elso=0
    maxérték = 0
    opt=0
    for i in np.linspace(min, max, db):
        d = Decimal(i)
        device.MoveTo(d, paddle, 60000)
        lista=[]
        for j in range(1,5):
            adat2 = zmq_exec(tc, f"INPUt{j}:COUNter?")
            adat = int(adat2)
            if(j==1):
                adat_elso=adat
            lista.append(adat)
        adatok.append(lista)
        probalk.append(i)
        print(f"Fok:{round(i,2)} Mérés:{lista[0]}")
        time.sleep(0.2)
        if adat_elso > maxérték:
            maxérték = adat_elso
            opt = i

    d = Decimal(opt)
    device.MoveTo(d, paddle, 60000)
    print(f'OPTIMUM: {round(opt,2)}')

    return [probalk,adatok,opt]
def uj_min(a,mennyivel): #kell majd#
    c=a-mennyivel
    if(c<0):
        c=0
    return c

def uj_max(a,mennyivel): #kell majd#
    c=a+mennyivel
    if(c>170):
        c=170
    return c


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--acquisitions",
        type=int,
        help="number of counter acquisitions",
        metavar=("N"),
        default=DEFAULT_NUMBER_OF_ACQUISITIONS,
    )
    parser.add_argument(
        "--address",
        type=str,
        help="Time Controller address",
        metavar=("IP"),
        default=DEFAULT_TC_ADDRESS,
    )
    parser.add_argument(
        "--integration",
        type=int,
        help="counter integration time in ps",
        metavar="PS",
        default=DEFAULT_COUNTERS_INTEGRATION_TIME,
    )
    parser.add_argument(
        "--counters",
        type=str,
        nargs="+",
        choices=COUNT_OVER_TIME_INPUTS,
        help=f"input counts to acquire (choices {COUNT_OVER_TIME_INPUTS})",
        metavar="INPUT",
        default=DEFAULT_COUNTERS,
    )
    parser.add_argument(
        "--save",
        type=str,
        help="save counter trace in a csv file",
        metavar="FILEPATH",
        dest="counts_filepath",
        default=DEFAULT_COUNTS_FILEPATH,
    )
    parser.add_argument(
        "--log-path",
        type=Path,
        help="store output in log file",
        metavar=("FULLPATH"),
        default=DEFAULT_LOG_PATH,
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
        filename=args.log_path
    )

    """----------------------------------- KONTROLLER------------------------------- """
    """The main entry point for the application"""

    # Uncomment this line if you are using
    #SimulationManager.Instance.InitializeSimulations()

    try:
        # print(GenericMotorCLI.ControlParameters.JogParametersBase.JogModes.SingleStep)
        # Create new device
        serial_no = str("38290024")

        DeviceManagerCLI.BuildDeviceList()

        device = Polarizer.CreatePolarizer(serial_no)

        print(DeviceManagerCLI.GetDeviceList())
        # Connect, begin polling, and enable
        print("Connecting to MPC320")
        device.Connect(serial_no)

        time.sleep(0.25)
        device.StartPolling(250)
        time.sleep(0.25)  # wait statements are important to allow settings to be sent to the device

        device.EnableDevice()
        time.sleep(0.25)  # Wait for device to enable

        # Get Device information
        device_info = device.GetDeviceInfo()
        print(device_info.Description)

        # Wait for Settings to Initialise
        if not device.IsSettingsInitialized():
            device.WaitForSettingsInitialized(10000)  # 10 second timeout
            assert device.IsSettingsInitialized() is True
    except Exception as e:
        print(e)


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

        # plot_histograms(
        #     counts,
        #     actual_integration_time,
        #     title="Input counts over time",
        # )
        "-------------------------------------------------"
        # paddle = PolarizerPaddles.Paddle1
        # adatok=[]
        # fokok=[]
        # for i in np.linspace(0, 170,10):
        #     #for i in range(1,5):
        #     #adat=zmq_exec(tc, f"HIST{i}:DATA?")
        #
        #     d = Decimal(i)
        #     device.MoveTo(d, paddle, 60000)
        #     time.sleep(0.5)
        #     adat2 = zmq_exec(tc, f"INPUt{1}:COUNter?")  # fontos#
        #     # print(adat)
        #     print(adat2)
        #     fokok.append(i)
        #     adatok.append(int(adat2))
        # plt.plot(np.array(fokok), np.array(adatok))
        # adatok = []
        # fokok = []
        # paddle = PolarizerPaddles.Paddle2
        # for i in np.linspace(0, 170, 10):
        #     d = Decimal(i)
        #     device.MoveTo(d, paddle, 60000)
        #     time.sleep(0.5)
        #     adat2 = zmq_exec(tc, f"INPUt{1}:COUNter?")  # fontos#
        #     print(adat2)
        #     fokok.append(i)
        #     adatok.append(int(adat2))
        #
        # plt.plot(np.array(fokok), np.array(adatok))
        # adatok = []
        # fokok = []
        # paddle = PolarizerPaddles.Paddle3
        # for i in np.linspace(0, 170, 10):
        #     d = Decimal(i)
        #     device.MoveTo(d, paddle, 60000)
        #     time.sleep(0.5)
        #     adat2 = zmq_exec(tc, f"INPUt{1}:COUNter?")  # fontos#
        #     print(adat2)
        #     fokok.append(i)
        #     adatok.append(int(adat2))
        #
        # plt.plot(np.array(fokok),np.array(adatok))
        # plt.show()
        # #RANDOM PONTOK
        # adatok=[]
        # pontok=10
        # paddle1 = PolarizerPaddles.Paddle1
        # paddle2 = PolarizerPaddles.Paddle2
        # paddle3 = PolarizerPaddles.Paddle3
        # fokok = np.random.rand(pontok, 3) * 170
        # probalkozasok=[]
        # for i in range(pontok):
        #     fok1 = int(fokok[i, 0])
        #     fok2 = int(fokok[i, 1])
        #     fok3 = int(fokok[i, 2])
        #
        #     d1 = Decimal(fok1)
        #     d2 = Decimal(fok2)
        #     d3 = Decimal(fok3)
        #
        #     device.MoveTo(d1, paddle1, 60000)
        #     device.MoveTo(d2, paddle2, 60000)
        #     device.MoveTo(d3, paddle3, 60000)
        #     time.sleep(0.5)
        #
        #     probalkozasok.append(i+1)
        #     adat2 = zmq_exec(tc, f"INPUt{1}:COUNter?")
        #     adatok.append(int(adat2))
        #     print(fokok[i],adat2)
        # plt.plot(probalkozasok,adatok)
        # plt.show()


        ##OPTIMUM
        adatok=[]
        probalk=[]
        optimum=[0,0,0]
        paddle1 = PolarizerPaddles.Paddle1
        paddle2 = PolarizerPaddles.Paddle2
        paddle3 = PolarizerPaddles.Paddle3

        min=[0,0,0]
        max=[170,170,170]



        for j in range(2):
            fokok = []
            adatok2 = []
            probalk,adatok,optimum[0]=optimum_kereso(device,tc,paddle1,min[0],max[0],10)
            fokok.append(probalk)
            adatok2.append(adatok)
            probalk, adatok, optimum[1] = optimum_kereso(device, tc, paddle2, min[1], max[1], 10)
            fokok.append(probalk)
            adatok2.append(adatok)
            probalk, adatok, optimum[2] = optimum_kereso(device, tc, paddle3, min[2], max[2], 10)
            fokok.append(probalk)
            adatok2.append(adatok)
            adatok3 = np.array(adatok2)
            for c in range(4):
                fig = plt.figure(j*4+c+1)
                for v in range(3):
                    plt.plot(fokok[v], adatok3[:,:,c][v])
                fig.suptitle(f'{c + 1}. detektor')
                plt.draw()

            for i in range(3):
                min[i]=uj_min(optimum[i],20)
                max[i]=uj_max(optimum[i],20)



        #plt.show()



        opt=[0,0,0]
        minimum=[0,0,0]
        maximum=[170,170,170]

        adatok=np.array(adatok)


        plt.show()



    except AssertionError as e:
        logger.error(e)
        sys.exit(1)

    except ConnectionError as e:
        logger.exception(e)
        sys.exit(1)

    sys.exit(0)


    # """------------------------------------------------VEZÉRLÉS-------------------------------------------"""
    # S_cel = Svec(np.pi / 2, 0)  # Cél beállítás    "X"
    # random_pontok_szama = 10
    # print(S_cel)
    #
    # "-------------0-ba állítás (ha kell)-----------------------"
    # # d = Decimal(0)
    # # paddle = PolarizerPaddles.Paddle2
    # # device.MoveTo(d, paddle, 60000)
    # # paddle = PolarizerPaddles.Paddle1
    # # device.MoveTo(d, paddle, 60000)
    # # paddle = PolarizerPaddles.Paddle3
    # # device.MoveTo(d, paddle, 60000)
    # # min1=0
    # # min2=0
    # # min3=0
    # # max1=170
    # # max2=170
    # # max3=170
    # "--------------------------------------------------------"
    #









if __name__ == "__main__":
    main()