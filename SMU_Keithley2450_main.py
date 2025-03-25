import argparse
import time
from SMU_controller import SMUController, SMUSwitch
from SMU_ramp_controller import RampController
from SMU_monitoring import SMUMonitoring

def main():
    parser = argparse.ArgumentParser(description="Ramp voltage of the SMU.")
    #parser.add_argument('--hv', type=float, required=True, help="Target high voltage (HV).")
    parser.add_argument('--hv', type=float, help="Target high voltage (HV).")
    parser.add_argument('--step', type=float, default=0.5, help="Voltage step increment.")
    parser.add_argument('--delay', type=float, default=0.1, help="Delay between voltage steps.")
    args = parser.parse_args()

    RESOURCE_NAME = "TCPIP0::169.254.91.1::inst0::INSTR"

    # Create SMUController instance
    smu = SMUController(RESOURCE_NAME)
    smu.configure_smu()


    # SMUSwitch to power ON/OFF and check SMU status 
    # smu_power = SMUSwitch(smu.inst)
    # smu_power.power_on()  # Power on the SMU
    # time.sleep(2)  # Wait for a bit
    # smu_power.get_status()  # Check the status
    # time.sleep(2)
    # smu_power.power_off()  # Power off the SMU
    


    # Perform the voltage ramp only if --hv is specified
    if args.hv is not None:
        ramp = RampController(smu)
        ramp.ramp_voltage(args.hv, args.step, args.delay)

    # Start monitoring current after ramping
    monitor = SMUMonitoring(smu.inst, interval=1)
    monitor.start()
    time.sleep(2)

    # Wait for some time while monitoring
    input("Monitoring... Press Enter to stop.\n")
    monitor.stop()  # Stop the monitoring when done
    print("Stop monitoring.")

    # Close connection
    smu.close()

if __name__ == '__main__':
    main()