import time
import clr
import sys


clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.PolarizerCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.PolarizerCLI import *
from System import Decimal


def main():

    """--------------------------------Polariméter-----------------------------"""
    # Load DLL library
    lib = cdll.LoadLibrary("C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLPAX_64.dll")

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
        serial_no = str("38000002")

        DeviceManagerCLI.BuildDeviceList()

        device = Polarizer.CreatePolarizer(serial_no)

        print(DeviceManagerCLI.GetDeviceList())
        # Connect, begin polling, and enable
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

        print("Vezérlés")









        """---------------------------------------------------------------------------------------------------"""




        device.StopPolling()
        device.Disconnect(True)

        """-----------Polariméter---------"""
        # Close
        lib.TLPAX_close(instrumentHandle)
        print("Connection to PAX1000 closed.")
        """-------------------------------"""
    except Exception as e:
        print(e)

    #SimulationManager.Instance.UninitializeSimulations()
    return None


if __name__ == "__main__":
    main()

