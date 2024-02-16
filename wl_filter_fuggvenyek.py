import time
import numpy as np
import sys
import logging
import csv
import matplotlib.pyplot as plt
import datetime
import os

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



def kiir(s,db):
    for i in range(db):
        print(s.readline(100).decode('utf-8'))


def csatlakozas_lekerdezes(s):
    s.write("dev?\r\n".encode('utf-8'))
    kiir(s,3)
    return

def wl_frekvencia_beallitas(s):
    s.write("FC\r\n".encode('utf-8'))
    return

def hullamhossz_beallitas(s,hullamhossz):
    s.write(f"wl{hullamhossz-1}\r\n".encode('utf-8'))
    kiir(s,2)
    time.sleep(0.2)

def hullamhossz_lekerdezes(s):
    s.write("wl?\r\n".encode('utf-8'))
    kiir(s,2)

def detektor_meres(tc):
    mert_adatok = []
    for j in range(1, 5):
        adat2 = zmq_exec(tc, f"INPUt{j}:COUNter?")
        adat = int(adat2)
        mert_adatok.append(adat)
    print(mert_adatok[3])
    return mert_adatok


def frekvencitartomany_vegigmerese(s,kezdet,vege,tc):
    hullamhosszak=[]
    beutes_szamok=[]

    for hullamhossz in np.linspace(kezdet,vege,int((vege-kezdet)/0.15)):
        hullamhossz_beallitas(s,hullamhossz)
        #hullamhossz_lekerdezes(s)
        time.sleep(2)
        'mérés'
        beutes_szam=detektor_meres(tc)

        hullamhosszak.append(hullamhossz)
        beutes_szamok.append(beutes_szam)

    return  [hullamhosszak,beutes_szamok]




def vegigmeres_csv(hullamhosszak,beutes_szamok,message):
    filepath="C:\\Users\\KNL2022\\PycharmProjects\\Poincare\\csvk\\hullamhossz_vegigmeres.csv"

    with open(filepath, 'a', newline="") as csvfile:
        writer_object = csv.writer(csvfile, delimiter=";")
        writer_object.writerow(["Start: "+message])
        for i in range(len(hullamhosszak)):
            lista = []
            lista.append(hullamhosszak[i])
            lista.append(beutes_szamok[i][3]) #negyedik detektor adatait
            writer_object.writerow(lista)
            print(lista)

        csvfile.close()
    return


def plot_and_save(hullamhosszak,beutes_szamok):
    beutesek=np.array(beutes_szamok)

    fig = plt.figure()
    plt.plot(hullamhosszak, beutesek[:,3])

    # Create a new directory with the current timestamp
    current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")


    # Save figure in the created directory
    fig_name = f"C:/Users/KNL2022/PycharmProjects/Poincare/képek/vegigmeres_{current_time}.png"
    plt.savefig(fig_name)
    plt.draw()
