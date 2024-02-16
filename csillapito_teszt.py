import time
import sys
import argparse
import logging
from pathlib import Path
import csv  # Új!!! az adatok CSV-fájlba mentéséhez
from datetime import datetime
import pyvisa
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
import threading
import keyboard

sys.path.append(str(Path("C:\\Users\\KNL2022\\Documents\\TimeController_V1_10_0\\Examples\\Python")))
from utils.common import connect, assert_arg_range
from utils.acquisitions import (
    setup_input_counts_over_time_acquisition,
    acquire_counts_over_time,
    save_counts_over_time,
    COUNT_OVER_TIME_INPUTS,
)
from utils.common import zmq_exec
from utils.plot import plot_histograms

max_photon_count = 10000


def connect_to_attenuator():
    rm = pyvisa.ResourceManager()
    mn939c = rm.open_resource('GPIB0::2::INSTR')
    return mn939c


def set_attenuation(instrument, attenuation):
    if instrument:
        command = f"A{int(attenuation)}00"
        instrument.write(command)
        return True
    return False
def set0_attenuation(instrument):
    if instrument:
        command = f"A0000"
        instrument.write(command)
        return True
    return False

def control_attenuator_based_on_photons(tc, max_photon_count):
    attenuator = connect_to_attenuator()
    running = True

    while running:
        num_adat = int(zmq_exec(tc, f"INPUt{1}:COUNter?"))

        if num_adat >= max_photon_count:
            set_attenuation(attenuator, 60.0)  # Beállítjuk a csillapást 60 dB-re
            print("Fotonszám meghaladta az 1 000 000-et, csillapítás 60 dB-re állítva!")
            running = False
