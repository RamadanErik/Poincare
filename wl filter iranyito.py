import serial
import datetime
from wl_filter_fuggvenyek import *


# import tkinter as tk
# import tkinter.ttk as ttk
#
# window = tk.Tk()
# greeting = tk.Label(text="Hello, Tkinter")
# greeting.pack()
# label = tk.Label(
#     text="Hello, Tkinter",
#     fg="white",
#     bg="black",
#     width=10,
#     height=10
# )
# label.pack()
# button = tk.Button(
#     text="Click me!",
#     width=25,
#     height=5,
#     bg="blue",
#     fg="yellow",
# )
# button.pack()
# window.mainloop()

def main():

    tc=time_controller_csatlakozas()


    s = serial.Serial('COM4', 115200, timeout=10)
    #    s.dtr = False

    csatlakozas_lekerdezes(s)
    wl_frekvencia_beallitas(s)

    idokezdet = datetime.datetime.now()

    #hullamhossz_beallitas(s,1551)

    message="BME, Temp=38.7, Trun = 9h, Ch=2"

    hullamhosszak,beutes_szamok=frekvencitartomany_vegigmerese(s,1548,1552,tc)
    vegigmeres_csv(hullamhosszak,beutes_szamok,message)
    plot_and_save(hullamhosszak,beutes_szamok)


    idovege=datetime.datetime.now()
    print()
    print(idovege-idokezdet)

    s.close()

    sys.exit(0)


if __name__ == "__main__":
    main()


