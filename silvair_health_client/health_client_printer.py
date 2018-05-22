import io
import enum

from silvair_otau_demo.console_out import ConsoleOut


class HealthFaults(enum.IntEnum):
  NO_FAULT                 = 0x00
  BATTERY_LOW_WARN         = 0x01
  BATTERY_LOW_ERR          = 0x02
  SUPPLY_VOLTAGE_LOW_WARN  = 0x03
  SUPPLY_VOLTAGE_LOW_ERR   = 0x04
  SUPPLY_VOLTAGE_HIGH_WARN = 0x05
  SUPPLY_VOLTAGE_HIGH_ERR  = 0x06
  POWER_INTERRUPTED_WARN   = 0x07
  POWER_INTERRUPTED_ERR    = 0x08
  NO_LOAD_WARN             = 0x09
  NO_LOAD_ERR              = 0x0A
  OVERLOAD_WARN            = 0x0B
  OVERLOAD_ERR             = 0x0C
  OVERHEAT_WARN            = 0x0D
  OVERHEAT_ERR             = 0x0E
  CONDENSATION_WARN        = 0x0F
  CONDENSATION_ERR         = 0x10
  VIBRATION_WARN           = 0x11
  VIBRATION_ERR            = 0x12
  CONFIGUTATION_WARN       = 0x13
  CONFIGUTATION_ERR        = 0x14
  ELEMENT_NOT_CAL_WARN     = 0x15
  ELEMENT_NOT_CAL_ERR      = 0x16
  MEMORY_WARN              = 0x17
  MEMORY_ERR               = 0x18
  SELF_TEST_WARN           = 0x19
  SELF_TEST_ERR            = 0x1A
  INPUT_TOO_LOW_WARN       = 0x1B
  INPUT_TOO_LOW_ERR        = 0x1C
  INPUT_TOO_HIGH_WARN      = 0x1D
  INPUT_TOO_HIGH_ERR       = 0x1E
  INPUT_NO_CHANGE_WARN     = 0x1F
  INPUT_NO_CHANGE_ERR      = 0x20
  ACTUATOR_BLOCKED_WARN    = 0x21
  ACTUATOR_BLOCKED_ERR     = 0x22
  HOUSING_OPENED_WARN      = 0x23
  HOUSING_OPENED_ERR       = 0x24
  TAMPER_WARN              = 0x25
  TAMPER_ERR               = 0x26
  DEVICE_MOVED_WARN        = 0x27
  DEVICE_MOVED_ERR         = 0x28
  DEVICE_DROPPED_WARN      = 0x29
  DEVICE_DROPPED_ERR       = 0x2A
  OVERFLOW_WARN            = 0x2B
  OVERFLOW_ERR             = 0x2C
  EMPTY_WARN               = 0x2D
  EMPTY_ERR                = 0x2E
  INTERNAL_BUS_WARN        = 0x2F
  INTERNAL_BUS_ERR         = 0x30
  MECHANISM_JAMMED_WARN    = 0x31
  MECHANISM_JAMMED_ERR     = 0x32
  RFU_START                = 0x33
  RFU_END                  = 0x7F
  VENDOR_SPECIFIC_START    = 0x80
  VENDOR_SPECIFIC_END      = 0xFF


class HealthClientStatusPrinter:
    """ Health Client Status Printer """

    def __init__(self, console_out: ConsoleOut):
        """ Initialize Health Client Status Printer

        :param  console_out: ConsoleOut, Console output.
        :return              None
        """
        self._console_out = console_out

    def print_attention_status(self, mesh_command: bytes):
        status = self.__parse_attention_status(io.BytesIO(mesh_command))
        self._console_out.print_standard_message("Attention: {} [s]".format(status["attention"]))

    def print_period_status(self, mesh_command: bytes):
        status = self.__parse_period_status(io.BytesIO(mesh_command))
        self._console_out.print_standard_message("Fast Period Divider: {} (value 2^n: {})".format(status["period"], 
                                                                                          (1 << status["period"])))

    def print_current_status(self, mesh_command: bytes):
        status = self.__parse_generic_status(io.BytesIO(mesh_command))
        gen_status_str = self._create_generic_status_str(status)

        self._console_out.print_standard_message("Current Status:\n\t{}\n".format(gen_status_str))

    def print_fault_status(self, mesh_command: bytes):
        status = self.__parse_generic_status(io.BytesIO(mesh_command))
        gen_status_str = self._create_generic_status_str(status)

        self._console_out.print_standard_message("Fault Status: \n\t{}\n".format(gen_status_str))

    def __parse_attention_status(self, stream):
        return {"attention": int.from_bytes(stream.read(1), byteorder='little')}
    
    def __parse_period_status(self, stream):
        return {"period": int.from_bytes(stream.read(1), byteorder='little')}

    def __parse_generic_status(self, stream):
        test_id = int.from_bytes(stream.read(1), byteorder='little')
        company_id = int.from_bytes(stream.read(2), byteorder='little')
        
        left_bytes = len(stream.getvalue()) - stream.tell()
        faults = stream.read(left_bytes - 2)
        src_addr = int.from_bytes(stream.read(2), byteorder='little')

        status = {
            "test_id": test_id,
            "company_id": company_id,
            "faults": faults,
            "src_addr": src_addr
        }

        return status

    def _create_generic_status_str(self, status):
        src_addr_str = "src_addr: 0x{:04x}".format(status["src_addr"])
        test_id_str = "test_id: {}".format(status["test_id"])
        company_id_str = "company_id: 0x{:04x}".format(status["company_id"])
        faults_str = "faults: [{}]".format(", ".join([HealthFaults(fault).name for fault in status["faults"]]))

        return ",\n\t".join([src_addr_str, test_id_str, company_id_str, faults_str])
