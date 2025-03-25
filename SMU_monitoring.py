from rich.console import Console
from rich.table import Table
from rich.live import Live
import time
import threading

"""
SMU Monitoring Script

This script defines the `SMUMonitoring` class, which continuously monitors 
the voltage and current of a Source Measure Unit (SMU) and displays the values 
in a dynamic table in the terminal.

Features:
- Reads voltage and current values from the SMU at regular intervals.
- Displays the data in a formatted table using the Rich library.
- Runs the monitoring process in a separate thread.
- Stops monitoring when requested.

Usage:
1. Create an instance of `SMUMonitoring` by passing a valid SMU instrument connection.
2. Call `start()` to begin monitoring.
3. Call `stop()` to terminate monitoring when needed.

Dependencies:
- Requires the `rich` library for terminal visualization.
"""

class SMUMonitoring:
    def __init__(self, inst, interval=1):
        self.inst = inst
        self.interval = interval
        self.running = False

    def read_current_voltage(self):
        """Read current and voltage from the SMU"""
        try:
            voltage = float(self.inst.query("MEAS:VOLT?"))  # Query voltage
            current = float(self.inst.query("MEAS:CURR?"))  # Query current
            return voltage, current
        except Exception:
            return None, None

    def format_value(self, value, unit):
        """Format the value with the appropriate unit scaling."""
        if unit == "A":
            if abs(value) >= 1e-3:
                return f"{value * 1e3:.3f} mA"
            elif abs(value) >= 1e-6:
                return f"{value * 1e6:.3f} µA"
            else:
                return f"{value * 1e9:.3f} nA"
        elif unit == "V":
            if abs(value) >= 1:
                return f"{value:.3f} V"
            else:
                return f"{value * 1e3:.3f} mV"
        return f"{value:.3f} {unit}"

    def monitoring_task(self):
        console = Console()
        with Live(auto_refresh=False) as live:
            while self.running:
                voltage, current = self.read_current_voltage()
                table = Table(title="SMU Monitoring")
                table.add_column("Parameter", justify="left", style="cyan")
                table.add_column("Value", justify="right", style="bold")

                if voltage is not None and current is not None:
                    table.add_row("Voltage", self.format_value(voltage, "V"))
                    table.add_row("Current", self.format_value(current, "A"))
                else:
                    table.add_row("Error", "Failed to read values")

                live.update(table, refresh=True)
                time.sleep(self.interval)

    def start(self):
        """Start the monitoring in a separate thread."""
        self.running = True
        self.thread = threading.Thread(target=self.monitoring_task)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """Stop the monitoring."""
        self.running = False
        self.thread.join()
