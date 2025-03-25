import time
import sys
import numpy as np
from SMU_controller import SMUController

"""
RampController for SMU Voltage Control

This script provides a class, RampController, designed to safely ramp the output voltage 
of a Source Measurement Unit (SMU) to a target value. It ensures smooth transitions to 
prevent sudden voltage changes that could damage the device under test (DUT). 

Features:
- Implements voltage ramping with configurable step size and delay.
- Includes safety checks to prevent overvoltage conditions (limits voltage to 40V max).
- Prevents setting negative high voltage values.
- Reads and displays real-time voltage and current during the ramping process.

Usage:
1. Initialize the RampController with an instance of SMUController.
2. Call `ramp_voltage(end_voltage, step, delay)` to perform a controlled ramp.

Note:
- If the current voltage is already equal to the target voltage, the process exits.
- The voltage ramping is performed in small increments to ensure stability.
 
"""


class RampController:
    def __init__(self, smu: SMUController):
        """Initialize with an instance of SMUController"""
        self.smu = smu

    def ramp_voltage(self, end_voltage, step=0.5, delay=0.1):
        """Perform safe voltage ramping"""
        
        # Safety check: Overprotection voltage threshold
        if abs(end_voltage) > 40:
            print("WARNING: HV set is higher than the Overprotection Voltage!")
            sys.exit(0)

        if end_voltage < 0:
            print("HV cannot be negative!")
            sys.exit(0)

        # Read the current voltage
        set_voltage = self.smu.get_voltage()
        print(f"Current voltage set: {set_voltage} V")
        time.sleep(1)

        # If the voltage is already set to the desired value, exit
        if set_voltage == end_voltage:
            print(f"Voltage is already set to {end_voltage} V")
            sys.exit(0)

        # Ramp up or down
        print(f"Ramping {'up' if set_voltage < end_voltage else 'down'} to {end_voltage} V")
        for volt in np.arange(set_voltage, end_voltage + (step if set_voltage < end_voltage else -step), step if set_voltage < end_voltage else -step):
            self.smu.set_voltage(volt)
            time.sleep(delay)
            current = self.smu.get_current()
            print(f"Voltage: {volt:.1f} V, Current: {current:.2e} A", end="\r")
            time.sleep(0.1)

        print("\nVoltage ramp completed.")