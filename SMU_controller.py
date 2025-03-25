import pyvisa as visa
import time
import sys


"""
SMUController and SMUSwitch for Instrument Control

This script provides two classes to interface with a Source Measurement Unit (SMU) using the 
VISA (Virtual Instrument Software Architecture) library. It enables communication with the SMU 
via USB, LAN, or GPIB to control voltage output and measure current.

Classes:
1. SMUController:
   - Handles connection and communication with the SMU.
   - Configures the SMU for voltage sourcing and current measurement.
   - Provides methods to set voltage, read voltage, and measure current.
   - Implements error handling for connection issues.

2. SMUSwitch:
   - Controls the power state of the SMU (turn on/off).
   - Checks whether the SMU output is enabled or disabled.
   - Provides error handling for communication failures.

Features:
- Initializes and configures the SMU for operation.
- Allows controlled voltage setting and real-time current measurement.
- Implements debugging steps for connection issues.
- Provides an interface to enable/disable the SMU output and check its status.

Usage:
1. Initialize the SMUController with the appropriate resource name.
2. Call `configure_smu()` to set up the instrument.
3. Use `set_voltage(voltage)` to set the output voltage.
4. Use `get_voltage()` and `get_current()` to read values.
5. Use `SMUSwitch` to power on/off and check the SMU output status.

Note:
- Ensure the correct VISA resource name is provided when initializing the SMU.
- The current limit is set to 300 µA to protect the device under test (DUT).

"""

class SMUController:
    def __init__(self, resource_name):
        """Initialize the connection to the instrument"""
        self.rm = visa.ResourceManager()
        # self.inst = self.rm.open_resource(resource_name)
        # print("Connected to:", self.inst.query("*IDN?"))
        try:
            # Try to open the resource
            self.inst = self.rm.open_resource(resource_name)
            print(f" ")
            print(f"Connected to: {self.inst.query('*IDN?')}")

        except visa.errors.VisaIOError as e:
            print("ERROR: Could not connect to the instrument.")
            print("Debugging steps:")
            print("   - Is the instrument powered on?")
            print("   - Is the correct resource name being used?")
            print("   - Try running `rm.list_resources()` to check available devices.")
            print("   - Ensure the instrument is connected via USB, LAN, or GPIB.")
            print(f"VISA Error Details: {e}")
            exit(1) 

    def configure_smu(self):
        """Configure the SMU settings"""
        print("Configuring SMU...")
        self.inst.write("SOUR:FUNC VOLT")  # Set source function to voltage
        self.inst.write("SOUR:VOLT:RANG 200")  # Set voltage range
        self.inst.write("SOUR:VOLT:ILIM 0.0003")  # Set current limit to 300 µA
        self.inst.write("SENS:FUNC 'CURR'")  # Set measurement function to current
        self.inst.write("SENS:CURR:RANG 0.001")  # Set current measurement range

    def get_voltage(self):
        """Return the current set voltage"""
        return float(self.inst.query("SOUR:VOLT?").strip())

    def get_current(self):
        """Measure and return the current value"""
        self.inst.write("*WAI")
        return float(self.inst.query("MEAS:CURR?").strip())

    def set_voltage(self, voltage):
        """Set the voltage of the SMU"""
        self.inst.write(f"SOUR:VOLT {voltage}")

    def close(self):
        """Close the connection to the instrument"""
        self.inst.close()


class SMUSwitch:
    def __init__(self, inst):
        self.inst = inst
        # self.rm = visa.ResourceManager()
        # self.inst = self.rm.open_resource(resource_name)

    def power_on(self):
        """
        Turn on the SMU by enabling the output.
        """
        try:
            self.inst.write("OUTP ON")
            print("SMU is powered ON.")
        except visa.VisaIOError as e:
            print(f"Error turning on SMU: {e}")
    
    def power_off(self):
        """
        Turn off the SMU by disabling the output.
        """
        try:
            self.inst.write("OUTP OFF")
            print("SMU is powered OFF.")
        except visa.VisaIOError as e:
            print(f"Error turning off SMU: {e}")
    
    def get_status(self):
        """
        Get the current status of the SMU (whether it's powered on or off).
        """
        try:
            status = self.inst.query("OUTP?").strip()
            if status == "1":
                print("SMU is currently ON.")
            else:
                print("SMU is currently OFF.")
        except visa.VisaIOError as e:
            print(f"Error checking SMU status: {e}")