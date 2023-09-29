"""------------------FÜGGVÉNYEK-----------------------"""
import csv
import numpy as np
import matplotlib
from pathlib import Path
import matplotlib.pyplot as plt
import time
import clr
import sys
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.PolarizerCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.PolarizerCLI import *
from System import Decimal

sys.path.append("C:\\Users\\KNL2022\\Documents\\TimeController_V1_10_0\\Examples\\Python")
from utils.common import zmq_exec
from utils.common import connect
from utils.acquisitions import (
    setup_input_counts_over_time_acquisition
)


def save_counts_to_csv(fokok2,adatok3,optimum,opt_ertek):
    filepath="C:\\Users\\KNL2022\\PycharmProjects\\Poincare\\csvk\\meres.csv"
    with open(filepath, 'a', newline="") as csvfile:
        writer_object = csv.writer(csvfile, delimiter=";")

        for i in range(len(fokok2)): #2
            seged_tomb = [0, 0, 0]
            for k in range(len(fokok2[0])):  # 3
                for j in range(len(fokok2[0][0][0])): #10
                    lista=[]
                    for paddle in range(3):
                        lista.append(int(fokok2[0][i][0][(seged_tomb[paddle])]))
                    seged_tomb[k]+=1
                    if seged_tomb[k]>=len(fokok2[0][0][0]):
                        seged_tomb[k]-=1
                    for detektor in range(4):
                        lista.append(adatok3[i][k][j][detektor])
                    writer_object.writerow(lista)
                    print(lista)

        csvfile.close()
    filepath = "C:\\Users\\KNL2022\\PycharmProjects\\Poincare\\csvk\\optimum.csv"
    with open(filepath, 'a', newline="") as csvfile:
        writer_object = csv.writer(csvfile, delimiter=";")
        lista=[]
        ts = time.time()
        ido = datetime.fromtimestamp(ts)

        for i in range(len(optimum)):
            lista.append(int(optimum[i]))
        for i in range(len(opt_ertek)):
            lista.append(int(opt_ertek[i]))
        lista.append([ido.year,ido.month,ido.day,ido.hour,ido.minute,ido.second,ido.microsecond])
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


def kontrollerhez_csatlakozas():
    try:
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

        paddle11 = PolarizerPaddles.Paddle1
        paddle22 = PolarizerPaddles.Paddle2
        paddle33 = PolarizerPaddles.Paddle3

        # Wait for Settings to Initialise
        if not device.IsSettingsInitialized():
            device.WaitForSettingsInitialized(10000)  # 10 second timeout
            assert device.IsSettingsInitialized() is True
    except Exception as e:
        print(e)
        sys.exit(1)
    return device, paddle11, paddle22, paddle33

def time_controller_csatlakozas():
    try:
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

def kereso_algoritmus_sima(device,tc,iteraciok_szama,db):
    optimum = [0, 0, 0]
    paddle1 = PolarizerPaddles.Paddle1
    paddle2 = PolarizerPaddles.Paddle2
    paddle3 = PolarizerPaddles.Paddle3
    min = [0, 0, 0]
    max = [170, 170, 170]
    fokok_ki=[]
    adatok_ki=[]
    for j in range(iteraciok_szama):
        fokok_ki.append([[],[],[]])
    for j in range(iteraciok_szama):
        fokok = []
        adatok2 = []
        probalk, adatok, optimum[0] = optimum_kereso(device, tc, paddle1, min[0], max[0], db)
        fokok.append(probalk)
        fokok_ki[j][0].append(probalk)
        adatok2.append(adatok)
        probalk, adatok, optimum[1] = optimum_kereso(device, tc, paddle2, min[1], max[1], db)
        fokok.append(probalk)
        fokok_ki[j][1].append(probalk)
        adatok2.append(adatok)
        probalk, adatok, optimum[2] = optimum_kereso(device, tc, paddle3, min[2], max[2], db)
        fokok.append(probalk)
        fokok_ki[j][2].append(probalk)
        adatok2.append(adatok)
        adatok3 = np.array(adatok2)
        adatok_ki.append(adatok3)
        for c in range(4):
            fig = plt.figure(j * 4 + c + 1)
            for v in range(3):
                plt.plot(fokok[v], adatok3[:, :, c][v])
            fig.suptitle(f'{c + 1}. detektor')
            plt.draw()

        for i in range(3):
            min[i] = uj_min(optimum[i], 20)
            max[i] = uj_max(optimum[i], 20)
    return fokok_ki,adatok_ki,optimum