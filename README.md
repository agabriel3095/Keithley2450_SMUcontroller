# Keithley2450_SMUcontroller
---------------------------------
# SMU Control and Monitoring

This project provides a Python interface to control and monitor a Source Measurement Unit (SMU) using `pyvisa`. It allows voltage ramping, real-time monitoring of current and voltage, and power management (turning the SMU on/off). The project also provides live updates of SMU parameters in the terminal using the `rich` library.

## Features

- **Voltage Ramp:** Safely ramp the SMU voltage up or down with specified step increments.
- **Real-time Monitoring:** Continuously monitor and display current and voltage measurements in the terminal with live updates.
- **Power Management:** Turn the SMU on and off programmatically and check its status.
- **Safety Checks:** Includes voltage limits to ensure safe operation.

## Requirements

- Python 3.x
- `pyvisa` for communication with the SMU
- `rich` for terminal-based live updates
- A compatible SMU (e.g., Keithley SMU)

## Installation

- Install the required libraries:
pip install pyvisa rich

## Usage
Running the Program:
You can use the script to control and monitor the SMU:

`python SMU_Keithley2450_main.py --hv 10 --step 0.5 --delay 0.1`

`--hv`: Target high voltage (in volts)

`--step`: Voltage step increment (default is 0.5 V)

`--delay`: Delay between voltage steps (default is 0.1 seconds)

The script will:
1. Configure the SMU;
2. Ramp the voltage to the specified value;
3. Start real-time monitoring of current and voltage.

It's also possible to power ON/OFF the SMU and check the status

Power Management

The SMU can be powered on and off using the SMUSwitch class methods.

`smu_power = SMUSwitch(smu.inst)`

`smu_power.power_on()  # Power on the SMU`

`smu_power.power_off()  # Power off the SMU`

## Monitoring

Monitoring of current and voltage is handled by the SMUMonitoring class. 
Example:

`monitor = SMUMonitoring(smu.inst, interval=1) #interval in seconds` 

`monitor.start()  # Start monitoring`

`monitor.stop()  # Stop monitoring`

## Troubleshooting

    Error: Could not connect to the instrument

        Ensure that the SMU is powered on and correctly connected (via USB, LAN, or GPIB).

        Verify that the correct resource name is used.

        Try using rm.list_resources() to check available devices.

## License

This project is open-source.


