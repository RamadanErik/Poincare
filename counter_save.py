import csv  # Új!!! az adatok CSV-fájlba mentéséhez
import logging
import sys
import time
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox

import keyboard

from csillapito_teszt import connect_to_attenuator, set_attenuation, set0_attenuation

sys.path.append(str(Path("C:\\Users\\KNL2022\\Documents\\TimeController_V1_10_0\\Examples\\Python")))
from utils.common import connect
from utils.common import zmq_exec

logger = logging.getLogger(__name__)
max_photon = 1000000
# Ebben tárolom a méréshez használt fájl nevét
DEFAULT_COUNTS_FILEPATH = "input_counts.csv"

# Ebben tárolom a fotonbeütések időpillanatait tartalmazó fájl nevét
DEFAULT_PHOTON_COUNTS_FILEPATH = "fotonbeutesek.csv"

# Alapértelmezett mérési idő másodpercekben
DEFAULT_MEASUREMENT_DURATION = 60

DEFAULT_NUMBER_OF_ACQUISITIONS = 5

DEFAULT_COUNTERS_INTEGRATION_TIME = 500000000000

DEFAULT_TC_ADDRESS = "169.254.104.112"

DEFAULT_COUNTERS = ["1", "2", "3", "4"]

filepath = "C:\\Users\\KNL2022\\PycharmProjects\\Poincare\\input_counts.csv"



# Saját függvény a fotonbeütések méréséhez
def save_counts_to_csv(counts):
    with open(filepath, 'a', newline="") as csvfile:
        writer_object = csv.writer(csvfile, delimiter=";")
        for count in counts:
            year, month, day, hour, minute, second, microsecond, counter, num_adat = count
            timestamp_str = f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}.{microsecond:06d}"
            writer_object.writerow([timestamp_str, counter, num_adat])
            print(timestamp_str, counter, num_adat)
        csvfile.flush()


def meres_fotonbeutes(tc, duration_time, max_photon_count, root):
    start_time = time.time()
    attenuator = connect_to_attenuator()
    set0_attenuation(attenuator)
    while time.time() - start_time < duration_time:
        time.sleep(1)
        keyboard.block_key("q")
        if keyboard.is_pressed("q"):
            set_attenuation(attenuator, 60.0)
            break
        adat = zmq_exec(tc, f"INPUt{4}:COUNter?")
        counts = []
        num_adat = int(adat)
        if num_adat >= max_photon_count:
            set_attenuation(attenuator, 60.0)  # Beállítjuk a csillapást 60 dB-re
            print(f"Fotonszám meghaladta a(z) {max_photon_count}-et, csillapítás 60 dB-re állítva!")
            break

        ts = time.time()
        date = datetime.fromtimestamp(ts)
        year, month, day, hour, minute, second, microsecond = date.year, date.month, date.day, date.hour, date.minute, date.second, date.microsecond
        counts.append([year, month, day, hour, minute, second, microsecond, 1, num_adat])
        root.status_label.config(text=f"Eltelt idő: {int(time.time() - start_time)} s")
        root.update()
        save_counts_to_csv(counts)


def start_measurement(root):
    try:
        duration_minutes = float(root.entry_duration.get())
        duration_time = duration_minutes * 60
        photon_count = int(root.entry_photon_count.get())
    except ValueError:
        messagebox.showerror("Hiba", "Kérlek adj meg érvényes számot a mérési időhöz!")
        return

    tc = connect(DEFAULT_TC_ADDRESS)
    meres_fotonbeutes(tc, duration_time, photon_count, root)
    attenuator = connect_to_attenuator()
    set_attenuation(attenuator, 60.0) # Mérés végén mindenképp legyen beállítva a biztonsági csillapítás


class MeasurementWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Fotonbeütés Mérés")
        frame = tk.Frame(self)
        frame.pack(padx=20, pady=20)
        label_duration = tk.Label(frame, text="Mérési idő (percben):")
        label_duration.pack()
        self.entry_duration = tk.Entry(frame)
        self.entry_duration.pack()
        label_photon_count = tk.Label(frame, text="Maximális fotonszám:")
        label_photon_count.pack()
        self.entry_photon_count = tk.Entry(frame)
        self.entry_photon_count.pack()
        self.start_button = tk.Button(frame, text="Indítás", command=lambda: start_measurement(self))
        self.start_button.pack()
        self.label_stop = tk.Label(frame, text="A mérés megállításához nyomd le a Q billentyűt!")
        self.label_stop.pack()
        self.status_label = tk.Label(self, text="")
        self.status_label.pack()


def main():
    root = MeasurementWindow()
    root.mainloop()


if __name__ == "__main__":
    main()
