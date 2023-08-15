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

def Svec(theta,phi):
    v = np.array([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)])
    return v

def Sdif(S1, S2):
    return np.linalg.norm(S1-S2)

def optimum(device, lib,instrumentHandle, S_cel,paddle,tart_eleje,tart_vege,lepeskoz):
    minimum_fok = -1
    minimum_hiba = -1
    lepesek = int((tart_vege-tart_eleje) / lepeskoz+1)
    kapcs=0

    x = []
    y = []
    z = []


    for i in np.linspace(tart_eleje, tart_vege, lepesek):
        d = Decimal(i)
        device.MoveTo(d, paddle, 60000)
        if(kapcs==0):
            kapcs=1
            time.sleep(0.5)
        time.sleep(0.1)
        revolutionCounter = c_int()
        scanID = c_int()
        time.sleep(0.5)
        lib.TLPAX_getLatestScan(instrumentHandle, byref(scanID))
        # S0 = c_double()  ### fontos sor
        S1 = c_double()  ### fontos sor
        S2 = c_double()  ### fontos sor
        S3 = c_double()  ### fontos sor

        lib.TLPAX_getStokesNormalized(instrumentHandle, scanID.value, byref(S1), byref(S2), byref(S3))  ### fontos sor
        # print(f"Svec=  {S1.value}, {S2.value}, {S3.value}\n")
        lib.TLPAX_releaseScan(instrumentHandle, scanID)

        S = np.array([S1.value, S2.value, S3.value])

        "-----kirajzoláshoz-----"
        x.append((S[0]).item())
        y.append((S[1]).item())
        z.append((S[2]).item())
        "----------------------"


        hiba = Sdif(S, S_cel)
        print(f"{round(i,2)} foknál a hiba: {round(hiba,5)}")
        if (hiba < minimum_hiba or minimum_fok==-1):
            minimum_hiba=hiba
            minimum_fok=i

    return [minimum_fok,x,y,z]

def optimum_rand(device, lib,instrumentHandle, S_cel,paddle1,paddle2,paddle3,pontok):
    beallitott_fokok=[] #új
    hibak_fokokhoz=[] #új
    kapcs=-1
    minimum_fokok = -1
    minimum_hiba = 3

    rosszfokok=[]
    rosszfok_hibak=[]
    jofokok=[]
    jofok_hibak=[]
    x = []
    y = []
    z = []
    i2=1
    while minimum_hiba > 0.3:
        fokok = np.random.rand(pontok,3)*170
        for i in range(pontok):
            fok1=int(fokok[i,0])
            fok2=int(fokok[i,1])
            fok3=int(fokok[i,2])
            rossz=False
            for j in range(len(rosszfokok)):
                maxhiba=20*1.41*(rosszfok_hibak[j]**(1/2))
                if (abs(fok1-rosszfokok[j][0])<maxhiba and abs(fok2-rosszfokok[j][1])<maxhiba and abs(fok3-rosszfokok[j][2])<maxhiba ):
                    i-=1
                    rossz=True
                    break
            if (not rossz):
                for j in range(len(jofokok)):
                    maxhiba2 = 80*jofok_hibak[j]
                    if (abs(fok1-jofokok[j][0])>maxhiba2 or abs(fok2-jofokok[j][1])>maxhiba2 or abs(fok3-jofokok[j][2])>maxhiba2 ):
                        i-=1
                        rossz=True
                        break

            if(not rossz):
                beallitott_fokok.append([fok1,fok2,fok3])
                d1 = Decimal(fok1)
                d2 = Decimal(fok2)
                d3 = Decimal(fok3)

                device.MoveTo(d1, paddle1, 60000)
                device.MoveTo(d2, paddle2, 60000)
                device.MoveTo(d3, paddle3, 60000)

                time.sleep(0.1)
                revolutionCounter = c_int()
                scanID = c_int()
                time.sleep(1.5)
                lib.TLPAX_getLatestScan(instrumentHandle, byref(scanID))
                # S0 = c_double()  ### fontos sor
                S1 = c_double()  ### fontos sor
                S2 = c_double()  ### fontos sor
                S3 = c_double()  ### fontos sor

                lib.TLPAX_getStokesNormalized(instrumentHandle, scanID.value, byref(S1), byref(S2), byref(S3))  ### fontos sor
                # print(f"Svec=  {S1.value}, {S2.value}, {S3.value}\n")
                lib.TLPAX_releaseScan(instrumentHandle, scanID)


                S = np.array([S1.value, S2.value, S3.value])

                "-----kirajzoláshoz-----"
                x.append((S[0]).item())
                y.append((S[1]).item())
                z.append((S[2]).item())
                "----------------------"


                hiba = Sdif(S, S_cel)
                hibak_fokokhoz.append(hiba)
                print(f"{i2}. vizsgálat: {fok1},{fok2},{fok3} fokoknál a hiba: {round(hiba,5)}")
                i2+=1 #Hanyadik vizsgálat
                if (hiba < minimum_hiba or kapcs==-1):
                    kapcs=1
                    minimum_hiba=hiba
                    minimum_fokok=fokok[i]
                if (hiba > 1.3 ):
                    rosszfokok.append([fok1,fok2,fok3])
                    rosszfok_hibak.append(hiba)
                if (hiba < 0.7):
                    jofokok.append([fok1,fok2,fok3])
                    jofok_hibak.append(hiba)
                if (minimum_hiba<0.2):
                    break

    return [minimum_fokok,x,y,z,beallitott_fokok,hibak_fokokhoz]

'kornyezet  megvizsgalasa'
def min_max_beallit(t,a):
    minimum=[0,0,0]
    maximum=[170,170,170]
    for i in range(3):
        minimum[i] = t[i] - 30
        if minimum[i] < 0:
            minimum[i] = 0
        maximum[i] = t[i] + 30
        if maximum[i] > 170:
            maximum[i] = 170

    return [minimum,maximum]

'MÉG NEM JÓ'
def kornyezet(device, lib,instrumentHandle, S_cel,paddle1,paddle2,paddle3,optimum,rogzitett,beallitott_fokok,hibak_fokokhoz):

    lista1=min_max_beallit(optimum,30)
    minimum=lista1[0]
    maximum=lista1[1]

    d1=Decimal(optimum[0])
    d2 = Decimal(optimum[1])
    d3 = Decimal(optimum[2])
    device.MoveTo(d1, paddle1, 60000)
    device.MoveTo(d2, paddle2, 60000)
    device.MoveTo(d3, paddle3, 60000)


    hanyszor=[4,4,4]
    hanyszor[rogzitett-1]=1

    kapcs=[1,1,1]
    fok1=optimum[0]
    fok2=optimum[1]
    fok3=optimum[2]

    for i in np.linspace(minimum[0], maximum[0], hanyszor[0]):
        if (rogzitett!=1):
            fok1=i
            d1=Decimal(i)
            device.MoveTo(d1, paddle1, 60000)
            time.sleep(0.1)
        for j in np.linspace(minimum[1], maximum[1], hanyszor[1]):
            if (rogzitett != 2):
                fok2=j
                d2=Decimal(j)
                device.MoveTo(d2, paddle2, 60000)
                time.sleep(0.1)

            for k in np.linspace(minimum[2], maximum[2], hanyszor[2]):
                if (rogzitett != 3):
                    fok3=k
                    d3=Decimal(k)
                    device.MoveTo(d3, paddle3, 60000)
                    time.sleep(0.1)
                revolutionCounter = c_int()
                scanID = c_int()
                lib.TLPAX_getLatestScan(instrumentHandle, byref(scanID))
                # S0 = c_double()  ### fontos sor
                S1 = c_double()  ### fontos sor
                S2 = c_double()  ### fontos sor
                S3 = c_double()  ### fontos sor

                lib.TLPAX_getStokesNormalized(instrumentHandle, scanID.value, byref(S1), byref(S2),
                                              byref(S3))  ### fontos sor
                lib.TLPAX_releaseScan(instrumentHandle, scanID)
                S = np.array([S1.value, S2.value, S3.value])
                hiba = Sdif(S, S_cel)
                beallitott_fokok.append([fok1, fok2, fok3])
                hibak_fokokhoz.append(hiba)
                print(f'{i},{j},{k},   {d1},{d2},{d3}   {beallitott_fokok},{hibak_fokokhoz}')


    return [beallitott_fokok,hibak_fokokhoz]





def uj_min(a,mennyivel):
    c=a-mennyivel
    if(c<0):
        c=0
    return c

def uj_max(a,mennyivel):
    c=a+mennyivel
    if(c>170):
        c=170
    return c

def rajz(x,y,z):  #EZ ÚJ dolog
    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Set the limits of the plot
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.set_zticks([-1, 0, 1])

    ax.set_xticklabels(['-1', '0', '1'])
    ax.set_yticklabels(['-1', '0', '1'])
    ax.set_zticklabels(['-1', '0', '1'])

    # Plot the sphere
    u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
    x_sphere = np.cos(u) * np.sin(v)
    y_sphere = np.sin(u) * np.sin(v)
    z_sphere = np.cos(v)
    ax.plot_surface(x_sphere, y_sphere, z_sphere, alpha=0.1)

    ax.set_xlabel('S2')
    ax.set_ylabel('S3')
    ax.set_zlabel('S1')

    # Szinezes
    colors = np.linspace(0, 1, len(x))
    # colormap = plt.cm.ScalarMappable(cmap='seismic')
    # colormap = plt.cm.ScalarMappable(cmap='hsv')
    colormap = plt.cm.ScalarMappable(cmap='cool')
    ax.scatter(y, z, x, c=colormap.to_rgba(colors), s=5)

    #pontok összekötése
    ax.plot(y, z, x, color='grey', linewidth=1)

    return
def main():
    """--------------------------------Polariméter-----------------------------"""
    # Load DLL library
    lib = cdll.LoadLibrary(r"C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLPAX_64.dll")

    # Detect and initialize PAX1000 device
    instrumentHandle = c_ulong()
    IDQuery = True
    resetDevice = False
    resource = c_char_p(b"")
    deviceCount = c_int()

    # Check how many PAX1000 are connected
    lib.TLPAX_findRsrc(instrumentHandle, byref(deviceCount))
    if deviceCount.value < 1:
        print("No PAX1000 device found.")
        exit()
    else:
        print(deviceCount.value, "PAX1000 device(s) found.")
        print("")

    # Connect to the first available PAX1000
    lib.TLPAX_getRsrcName(instrumentHandle, 0, resource)
    if (0 == lib.TLPAX_init(resource.value, IDQuery, resetDevice, byref(instrumentHandle))):
        print("Connection to first PAX1000 initialized.")
    else:
        print("Error with initialization.")
        exit()
    print("")

    # Short break to make sure the device is correctly initialized
    time.sleep(2)

    # Make settings
    lib.TLPAX_setMeasurementMode(instrumentHandle, 9)
    lib.TLPAX_setWavelength(instrumentHandle, c_double(1550e-9))  # hullámhossz beállítás
    lib.TLPAX_setBasicScanRate(instrumentHandle, c_double(60))
    lib.TLPAX_setPowerRange(instrumentHandle, c_double(0.01));

    # Check settings
    wavelength = c_double()
    lib.TLPAX_getWavelength(instrumentHandle, byref(wavelength))
    print("Set wavelength [nm]: ", wavelength.value * 1e9)
    mode = c_int()
    lib.TLPAX_getMeasurementMode(instrumentHandle, byref(mode))
    print("Set mode: ", mode.value)
    scanrate = c_double()
    lib.TLPAX_getBasicScanRate(instrumentHandle, byref(scanrate))
    print("Set scanrate: ", scanrate.value)
    print("")

    # Short break
    time.sleep(5)


    """----------------------------------- KONTROLLER------------------------------- """
    """The main entry point for the application"""

    # Uncomment this line if you are using
    SimulationManager.Instance.InitializeSimulations()

    try:
        #print(GenericMotorCLI.ControlParameters.JogParametersBase.JogModes.SingleStep)
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

        # # Before homing or moving device, ensure the motor's configuration is loaded
        # m_config = device.LoadMotorConfiguration(serial_no,
        #                                         DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
        #
        # m_config.DeviceSettingsName = "MTS50/M-Z8"
        #
        # m_config.UpdateCurrentConfiguration()
        #
        # device.SetSettings(device.MotorDeviceSettings, True, False)

        # print("Homing Actuator")
        # device.Home(60000)  # 10s timeout, blocking call
        #
        # f = 13.0
        # d = Decimal(f)
        # print(f'Device Homed. Moving to position {f}')
        # device.MoveTo(d, 60000)  # 10s timeout again
        # time.sleep(1)
        #
        # print(f'Device now at position {device.Position}')
        # time.sleep(1)

        # paddle = PolarizerPaddles.Paddle1
        # print("mozgatas")
        # device.MoveTo(d, paddle, 60000)
        # time.sleep(1)
        # print("Mozgatas2")
        # device.Home(paddle,60000)


        """------------------------------------------------VEZÉRLÉS-------------------------------------------"""
        S_cel = Svec(np.pi/2,np.pi/2)  #Cél beállítás
        random_pontok_szama=10
        print(S_cel)

        "-------------0-ba állítás (ha kell)-----------------------"
        # d = Decimal(0)
        # paddle = PolarizerPaddles.Paddle2
        # device.MoveTo(d, paddle, 60000)
        # paddle = PolarizerPaddles.Paddle1
        # device.MoveTo(d, paddle, 60000)
        # paddle = PolarizerPaddles.Paddle3
        # device.MoveTo(d, paddle, 60000)
        # min1=0
        # min2=0
        # min3=0
        # max1=170
        # max2=170
        # max3=170
        "--------------------------------------------------------"

        paddle1 = PolarizerPaddles.Paddle1
        paddle2 = PolarizerPaddles.Paddle2
        paddle3 = PolarizerPaddles.Paddle3
        print("Vezérlés:\n")

        print("Random pontokra beállítás")
        "Random helyekre beállítások"
        lista = optimum_rand(device,lib,instrumentHandle,S_cel,paddle1,paddle2,paddle3,random_pontok_szama)
        #lista=[[100,50,75],1,2,3,[[100,50,75]],[0.27024]]  ##########Töröld majd csak teszteléshez kell########
        opt1=int(lista[0][0])
        opt2=int(lista[0][1])
        opt3=int(lista[0][2])
        rajz(lista[1], lista[2], lista[3])
        beallitott_fokok=lista[4]
        hibak_fokokhoz=lista[5]


        d1 = Decimal(opt1)
        d2 = Decimal(opt2)
        d3 = Decimal(opt3)
        device.MoveTo(d1, paddle1, 60000)
        device.MoveTo(d2, paddle2, 60000)
        device.MoveTo(d3, paddle3, 60000)

        print(f"Optimum eddig: {round(opt1,2)},{round(opt2,2)},{round(opt3,2)} ")
        lepeskoz = 10

        min1 = uj_min(opt1, lepeskoz)
        min2 = uj_min(opt2, lepeskoz)
        min3 = uj_min(opt3, lepeskoz)
        max1 = uj_max(opt1, lepeskoz)
        max2 = uj_max(opt2, lepeskoz)
        max3 = uj_max(opt3, lepeskoz)

        lepeskoz/=5

        revolutionCounter = c_int()
        scanID = c_int()

        S1 = c_double()  ### fontos sor
        S2 = c_double()  ### fontos sor
        S3 = c_double()  ### fontos sor
        for i in range(0):

            paddle = PolarizerPaddles.Paddle2
            lista = optimum(device, lib,instrumentHandle, S_cel,paddle,min2,max2,lepeskoz)
            opt2 = lista[0]
            rajz(lista[1],lista[2],lista[3])
            d = Decimal(opt2)
            device.MoveTo(d,paddle,60000)
            print(f"Paddle2 optimum: {opt2} fok")


            paddle = PolarizerPaddles.Paddle3
            lista = optimum(device, lib, instrumentHandle, S_cel, paddle, min3,max3, lepeskoz)
            opt3 = lista[0]
            rajz(lista[1], lista[2], lista[3])
            d = Decimal(opt3)
            device.MoveTo(d, paddle, 60000)
            print(f"Paddle3 optimum: {opt3} fok")


            paddle = PolarizerPaddles.Paddle1
            lista = optimum(device, lib, instrumentHandle, S_cel, paddle, min1, max1, lepeskoz)
            opt1 = lista[0]
            rajz(lista[1], lista[2], lista[3])
            d = Decimal(opt1)
            device.MoveTo(d, paddle, 60000)
            print(f"Paddle1 optimum: {opt1} fok")

            min1 = uj_min(opt1,lepeskoz)
            min2 = uj_min(opt2, lepeskoz)
            min3 = uj_min(opt3, lepeskoz)
            max1 = uj_max(opt1,lepeskoz)
            max2 = uj_max(opt2, lepeskoz)
            max3 = uj_max(opt3, lepeskoz)

            lepeskoz/=5

            lib.TLPAX_getLatestScan(instrumentHandle, byref(scanID))
            lib.TLPAX_getStokesNormalized(instrumentHandle, scanID.value, byref(S1), byref(S2),
                                          byref(S3))  ### fontos sor
            # print(f"Svec=  {S1.value}, {S2.value}, {S3.value}\n")
            lib.TLPAX_releaseScan(instrumentHandle, scanID)
            time.sleep(0.5)

            S = np.array([S1.value, S2.value, S3.value])
            hiba = Sdif(S, S_cel)
            print(f"Pozíció: {round(opt1,2)}, {round(opt2,2)}, {round(opt3,2)}")
            print(f"Hiba: {round(hiba,5)}")







        lib.TLPAX_getLatestScan(instrumentHandle, byref(scanID))
        lib.TLPAX_getStokesNormalized(instrumentHandle, scanID.value, byref(S1), byref(S2), byref(S3))  ### fontos sor
        # print(f"Svec=  {S1.value}, {S2.value}, {S3.value}\n")
        lib.TLPAX_releaseScan(instrumentHandle, scanID)
        time.sleep(0.5)

        S = np.array([S1.value, S2.value, S3.value])
        hiba = Sdif(S, S_cel)
        print(f"Pozíció: {opt1}, {opt2}, {opt3}")
        print(f"Hiba: {hiba}")
        print(f"Beállított fokok: {beallitott_fokok}")
        print(f"Hibák a fokokhoz: {hibak_fokokhoz}")

        #Kocka
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim(0, 170)
        ax.set_ylim(0, 170)
        ax.set_zlim(0, 170)
        ax.set_xlabel('Elso')
        ax.set_ylabel('Masodik')
        ax.set_zlabel('Harmadik')
        szinek=np.array(hibak_fokokhoz)
        szinek=1-(szinek/2)
        data=np.array(beallitott_fokok)

        colormap = plt.cm.ScalarMappable(cmap='RdYlGn')
        ax.scatter(data[:,0], data[:,1], data[:,2], c=colormap.to_rgba(szinek))

        'három sík az optimum körül'
        optimum_hely=[opt1,opt2,opt3]

        beallitott_fokok1=[]
        hibak_fokokhoz1=[]

        [beallitott_fokok1,hibak_fokokhoz1]=kornyezet(device,lib,instrumentHandle,S_cel,paddle1,paddle2,paddle3,optimum_hely,1,beallitott_fokok1,hibak_fokokhoz1)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim(0, 170)
        ax.set_ylim(0, 170)
        ax.set_zlim(0, 170)
        ax.set_xlabel('Elso')
        ax.set_ylabel('Masodik')
        ax.set_zlabel('Harmadik')
        szinek = np.array(hibak_fokokhoz1)
        szinek=1-(szinek/2)
        data = np.array(beallitott_fokok1)
        colormap = plt.cm.ScalarMappable(cmap='RdYlGn')
        ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=colormap.to_rgba(szinek))

        beallitott_fokok1 = []
        hibak_fokokhoz1 = []
        [beallitott_fokok1, hibak_fokokhoz1] = kornyezet(device, lib, instrumentHandle, S_cel, paddle1, paddle2,
                                                         paddle3, optimum_hely, 2, beallitott_fokok1, hibak_fokokhoz1)


        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim(0, 170)
        ax.set_ylim(0, 170)
        ax.set_zlim(0, 170)
        ax.set_xlabel('Elso')
        ax.set_ylabel('Masodik')
        ax.set_zlabel('Harmadik')
        szinek = np.array(hibak_fokokhoz1)
        szinek=1-(szinek/2)
        data = np.array(beallitott_fokok1)
        colormap = plt.cm.ScalarMappable(cmap='RdYlGn')
        ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=colormap.to_rgba(szinek))

        beallitott_fokok1 = []
        hibak_fokokhoz1 = []
        [beallitott_fokok1, hibak_fokokhoz1] = kornyezet(device, lib, instrumentHandle, S_cel, paddle1, paddle2,
                                                         paddle3, optimum_hely, 3, beallitott_fokok1, hibak_fokokhoz1)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim(0, 170)
        ax.set_ylim(0, 170)
        ax.set_zlim(0, 170)
        ax.set_xlabel('Elso')
        ax.set_ylabel('Masodik')
        ax.set_zlabel('Harmadik')
        szinek = np.array(hibak_fokokhoz1)
        szinek=1-(szinek/2)
        data = np.array(beallitott_fokok1)
        colormap = plt.cm.ScalarMappable(cmap='RdYlGn')
        ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=colormap.to_rgba(szinek))

        """---------------------------------------------------------------------------------------------------"""

        idoveg = datetime.datetime.now()
        delta = idoveg - idokezdet
        print(delta)



        device.StopPolling()
        device.Disconnect(True)

        """-----------Polariméter---------"""
        # Close
        lib.TLPAX_close(instrumentHandle)
        print("Connection to PAX1000 closed.")
        """-------------------------------"""
        plt.show()
    except Exception as e:
        print(e)

    #SimulationManager.Instance.UninitializeSimulations()
    return None


if __name__ == "__main__":
    main()

