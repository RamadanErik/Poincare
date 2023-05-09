# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
"""An example that uses the .NET Kinesis Libraries to connect to a KDC."""
import os
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
    """The main entry point for the application"""

    # Uncomment this line if you are using
    #SimulationManager.Instance.InitializeSimulations()

    try:
        #print(GenericMotorCLI.ControlParameters.JogParametersBase.JogModes.SingleStep)
        # Create new device
        #serial_no = str("38000001")
        serial_no = str("38290024") #Eszköz

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
        f = 0
        d = Decimal(f)
        # print(f'Device Homed. Moving to position {f}')
        # device.MoveTo(d, 60000)  # 10s timeout again
        # time.sleep(1)
        #
        # print(f'Device now at position {device.Position}')
        # time.sleep(1)

        paddle = PolarizerPaddles.Paddle2
        print("mozgatas")
        device.MoveTo(d, paddle, 60000)
        time.sleep(1)
        print("Mozgatas2")
        #device.Home(paddle,60000)

        device.StopPolling()
        device.Disconnect(True)
    except Exception as e:
        print(e)

    #SimulationManager.Instance.UninitializeSimulations()
    return None


if __name__ == "__main__":
    main()