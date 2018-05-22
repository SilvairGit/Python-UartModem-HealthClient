from silvair_health_client.health_opcodes import HealthClientOpcodes

from silvair_uart_common_libs import messages


class HealthClient:
    """ Health Client """

    def __init__(self, sender, instance_index):
        """ Initalize Health Client

        :param sender:         Sender, Uart Sender.
        :param instance_index: int,    Model Instance Index.
        :return:               None
        """
        self._sender = sender
        self._instance_index = instance_index

    def send_attention_get(self):
        """ Send Attention Get message.

        :return: None
        """
        msg = messages.MeshMessageRequestMessage()
        msg.instance_index = self._instance_index
        msg.mesh_opcode = HealthClientOpcodes.ATTENTION_GET
        msg.mesh_command = bytes()

        self._sender.send_message(msg)

    def send_attention_set(self, attention_s, unack=False):
        """ Send Attention Set message.

        :param attention_s: int,  Attention time in seconds.
        :param unack:       bool, Unacknowledged message.
        :return:            None
        """
        msg = messages.MeshMessageRequestMessage()
        msg.instance_index = self._instance_index
        msg.mesh_command = int(attention_s).to_bytes(1, byteorder='little')

        if unack:
            msg.mesh_opcode = HealthClientOpcodes.ATTENTION_SET_UNACKNOWLEDGED
        else:
            msg.mesh_opcode = HealthClientOpcodes.ATTENTION_SET

        self._sender.send_message(msg)

    def send_fault_clear(self, company_id, unack=False):
        """ Send Fault Clear message

        :param company_id: str,  Company Id.
        :param unack:      bool, Unacknowledged message.
        :return:           None
        """
        msg = messages.MeshMessageRequestMessage()
        msg.instance_index = self._instance_index
        msg.mesh_command = int(company_id, 16).to_bytes(2, byteorder='little')

        if unack:
            msg.mesh_opcode = HealthClientOpcodes.FAULT_CLEAR_UNACKNOWLEDGED
        else:
            msg.mesh_opcode = HealthClientOpcodes.FAULT_CLEAR

        self._sender.send_message(msg)

    def send_fault_get(self, company_id):
        """ Send Fault Get message

        :param company_id: str,  Company Id.
        :return:           None
        """
        msg = messages.MeshMessageRequestMessage()
        msg.instance_index = self._instance_index
        msg.mesh_opcode = HealthClientOpcodes.FAULT_GET
        msg.mesh_command = int(company_id, 16).to_bytes(2, byteorder='little')
        
        self._sender.send_message(msg)

    def send_fault_test(self, company_id, test_id, unack=False):
        """ Send Fault Test message

        :param company_id: str,  Company Id.
        :param test_id:    str,  Test Id.
        :param unack:      bool, Unacknowledged message.
        :return:           None
        """
        msg = messages.MeshMessageRequestMessage()
        msg.instance_index = self._instance_index
        msg.mesh_command = bytearray()
        msg.mesh_command += int(test_id).to_bytes(1, byteorder='little')
        msg.mesh_command += int(company_id, 16).to_bytes(2, byteorder='little')

        if unack:
            msg.mesh_opcode = HealthClientOpcodes.FAULT_TEST_UNACKNOWLEDGED
        else:
            msg.mesh_opcode = HealthClientOpcodes.FAULT_TEST

        self._sender.send_message(msg)

    def send_period_get(self):
        """ Send Period Get message

        :return:           None
        """
        msg = messages.MeshMessageRequestMessage()
        msg.instance_index = self._instance_index
        msg.mesh_opcode = HealthClientOpcodes.PERIOD_GET
        msg.mesh_command = bytes()

        self._sender.send_message(msg)

    def send_period_set(self, fast_period_dividor, unack=False):
        """ Send Period Set message

        :param fast_period_dividor: str,  Fast Period Divider.
        :param unack:               bool, Unacknowledged message.
        :return:                    None
        """
        msg = messages.MeshMessageRequestMessage()
        msg.instance_index = self._instance_index
        msg.mesh_command = int(fast_period_dividor).to_bytes(1, byteorder='little')

        if unack:
            msg.mesh_opcode = HealthClientOpcodes.PERIOD_SET_UNACKNOWLEDGED
        else:
            msg.mesh_opcode = HealthClientOpcodes.PERIOD_SET

        self._sender.send_message(msg)
