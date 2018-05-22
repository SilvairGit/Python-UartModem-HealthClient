import time
import sys
import argparse

from silvair_uart_common_libs.message_types import ModelID, ModelDesc
from silvair_uart_common_libs.uart_common_classes import UartAdapter

from silvair_otau_demo.console_out import ConsoleOut
from silvair_otau_demo.dispatcher import Dispatcher, Sender
from silvair_otau_demo.uart_logic.uart_fsm_mgr import UART_FSM

from silvair_health_client.health_client import HealthClient
from silvair_health_client.health_client_cli import HealthClientCli
from silvair_health_client.health_opcodes import HealthClientOpcodes
from silvair_health_client.health_client_printer import HealthClientStatusPrinter
from silvair_health_client.health_client_evt_mgr import HealtClientEventMgr
from silvair_health_client.utils import ModelIdToInstanceIndexMapper, HealthClientOpcodesDispatcher


def create_uart_adapter_and_uart_fsm(com_port, event_mgr):
    """ Function creates instances required to connect to UART. """
    uart_adapter = UartAdapter(com_port)
    sender = Sender(uart_adapter)
    uart_fsm = UART_FSM(sender, event_mgr, default_models=(ModelDesc(ModelID.HealthClientID),))
    dfu_dispatcher = Dispatcher(uart_fsm, None)
    uart_adapter.register_observer(dfu_dispatcher)

    return uart_adapter, uart_fsm, sender


def parse_cli_args():
    """ Function parses passed command line arguments. """
    parser = argparse.ArgumentParser(description="Health Client CLI.")
    parser.add_argument("--port", metavar="/dev/ttyACM0", type=str, help="Serial port with connected UART Modem", required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_cli_args()

    try:
        console_out = ConsoleOut()
        hc_status_printer = HealthClientStatusPrinter(console_out)

        opcodes_disp = HealthClientOpcodesDispatcher({
            HealthClientOpcodes.CURRENT_STATUS: hc_status_printer.print_current_status,
            HealthClientOpcodes.FAULT_STATUS: hc_status_printer.print_fault_status,
            HealthClientOpcodes.ATTENTION_STATUS: hc_status_printer.print_attention_status,
            HealthClientOpcodes.PERIOD_STATUS: hc_status_printer.print_period_status
        })

        mid_to_ii_mapper = ModelIdToInstanceIndexMapper()
        event_mgr = HealtClientEventMgr(console_out, mid_to_ii_mapper, opcodes_disp)

        uart_adapter, uart_fsm, sender = create_uart_adapter_and_uart_fsm(args.port, event_mgr)
        uart_adapter.start()
        uart_fsm.start()

        print("Please reset device to map models into instance indexes.")
        print("Waiting for response from device...")

        timeout = 10
        timeout_time = time.time() + timeout

        while time.time() < timeout_time:
            if mid_to_ii_mapper.contains_model_id(ModelID.HealthClientID):
                break

            time.sleep(0.1)
        else:
            print("Could not get response from device within {}s.".format(timeout))
            sys.exit(1)

        # Take first registered Health Client model
        hc_instance_idx = mid_to_ii_mapper[ModelID.HealthClientID][0]

        print("Ready...")

        health_client_cli = HealthClientCli(console_out, HealthClient(sender, hc_instance_idx))
        health_client_cli.run()

    except KeyboardInterrupt:
        print("KeyboardInterrupt has been caught. Closing application...")
        uart_adapter.stop()
        
        sys.exit(0)
