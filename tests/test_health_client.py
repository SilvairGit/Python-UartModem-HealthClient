import binascii
import random
import unittest

from silvair_health_client.health_client import HealthClient
from silvair_health_client.health_opcodes import HealthClientOpcodes


def any_instance_index():
  return random.getrandbits(16)


def any_attention_s():
  return random.getrandbits(8)


def any_company_id():
  return binascii.hexlify(random.getrandbits(16).to_bytes(2, byteorder="little"))


def any_test_id():
  return random.getrandbits(8)


def any_fast_period_divider():
  return random.randrange(0, 15)


class BufferedSender:

  def __init__(self):
    self._sent_messages = []

  def send_message(self, msg):
    self._sent_messages.append(msg)

  @property
  def sent_messages(self):
    return self._sent_messages


class HealthClientTests(unittest.TestCase):

  def test_should_send_attention_get_when_send_attention_get_method_is_called(self):
    # GIVEN
    sender = BufferedSender()
    instance_index = any_instance_index()

    hc = HealthClient(sender, instance_index)

    # WHEN
    hc.send_attention_get()

    # THEN
    self.assertEqual(1, len(sender.sent_messages))
    
    msg = sender.sent_messages[0]
    self.assertEqual(instance_index, msg.instance_index)
    self.assertEqual(HealthClientOpcodes.ATTENTION_GET, msg.mesh_opcode)
    self.assertEqual(bytes(), msg.mesh_command)

  def test_should_send_attention_set_ack_when_send_attention_ack_method_is_called_with_unack_set_to_false(self):
    # GIVEN
    sender = BufferedSender()
    instance_index = any_instance_index()

    hc = HealthClient(sender, instance_index)

    attention_s = any_attention_s()

    # WHEN
    hc.send_attention_set(attention_s, False)

    # THEN
    self.assertEqual(1, len(sender.sent_messages))
    
    msg = sender.sent_messages[0]
    self.assertEqual(instance_index, msg.instance_index)
    self.assertEqual(HealthClientOpcodes.ATTENTION_SET, msg.mesh_opcode)
    self.assertEqual(attention_s.to_bytes(1, byteorder='little'), msg.mesh_command)


  def test_should_send_attention_set_unack_when_send_attention_ack_method_is_called_with_unack_set_to_true(self):
    # GIVEN
    sender = BufferedSender()
    instance_index = any_instance_index()

    hc = HealthClient(sender, instance_index)

    attention_s = any_attention_s()

    # WHEN
    hc.send_attention_set(attention_s, True)

    # THEN
    self.assertEqual(1, len(sender.sent_messages))
    
    msg = sender.sent_messages[0]
    self.assertEqual(instance_index, msg.instance_index)
    self.assertEqual(HealthClientOpcodes.ATTENTION_SET_UNACKNOWLEDGED, msg.mesh_opcode)
    self.assertEqual(attention_s.to_bytes(1, byteorder='little'), msg.mesh_command)

  def test_should_send_fault_clear_ack_when_send_fault_clear_method_is_called_with_unack_set_to_false(self):
    # GIVEN
    sender = BufferedSender()
    instance_index = any_instance_index()

    hc = HealthClient(sender, instance_index)

    company_id = any_company_id()

    # WHEN
    hc.send_fault_clear(company_id, False)

    # THEN
    self.assertEqual(1, len(sender.sent_messages))
    
    msg = sender.sent_messages[0]
    self.assertEqual(instance_index, msg.instance_index)
    self.assertEqual(HealthClientOpcodes.FAULT_CLEAR, msg.mesh_opcode)
    self.assertEqual(int(company_id, 16).to_bytes(2, byteorder='little'), msg.mesh_command)

  def test_should_send_fault_clear_unack_when_send_fault_clear_method_is_called_with_unack_set_to_true(self):
    # GIVEN
    sender = BufferedSender()
    instance_index = any_instance_index()

    hc = HealthClient(sender, instance_index)

    company_id = any_company_id()

    # WHEN
    hc.send_fault_clear(company_id, True)

    # THEN
    self.assertEqual(1, len(sender.sent_messages))
    
    msg = sender.sent_messages[0]
    self.assertEqual(instance_index, msg.instance_index)
    self.assertEqual(HealthClientOpcodes.FAULT_CLEAR_UNACKNOWLEDGED, msg.mesh_opcode)
    self.assertEqual(int(company_id, 16).to_bytes(2, byteorder='little'), msg.mesh_command)

  def test_should_send_fault_get_when_send_fault_get_method_is_called(self):
    # GIVEN
    sender = BufferedSender()
    instance_index = any_instance_index()

    hc = HealthClient(sender, instance_index)

    company_id = any_company_id()

    # WHEN
    hc.send_fault_get(company_id)

    # THEN
    self.assertEqual(1, len(sender.sent_messages))
    
    msg = sender.sent_messages[0]
    self.assertEqual(instance_index, msg.instance_index)
    self.assertEqual(HealthClientOpcodes.FAULT_GET, msg.mesh_opcode)
    self.assertEqual(int(company_id, 16).to_bytes(2, byteorder='little'), msg.mesh_command)

  def test_should_send_fault_test_ack_when_send_fault_test_method_is_called_with_unack_set_to_false(self):
    # GIVEN
    sender = BufferedSender()
    instance_index = any_instance_index()

    hc = HealthClient(sender, instance_index)

    company_id = any_company_id()
    test_id = any_test_id()

    # WHEN
    hc.send_fault_test(company_id, test_id, False)

    # THEN
    self.assertEqual(1, len(sender.sent_messages))
    
    msg = sender.sent_messages[0]
    self.assertEqual(instance_index, msg.instance_index)
    self.assertEqual(HealthClientOpcodes.FAULT_TEST, msg.mesh_opcode)

    mesh_command = bytearray()
    mesh_command += int(test_id).to_bytes(1, byteorder='little')
    mesh_command += int(company_id, 16).to_bytes(2, byteorder='little')
    self.assertEqual(bytes(mesh_command), msg.mesh_command)

  def test_should_send_fault_test_unack_when_send_fault_test_method_is_called_with_unack_set_to_true(self):
    # GIVEN
    sender = BufferedSender()
    instance_index = any_instance_index()

    hc = HealthClient(sender, instance_index)

    company_id = any_company_id()
    test_id = any_test_id()

    # WHEN
    hc.send_fault_test(company_id, test_id, True)

    # THEN
    self.assertEqual(1, len(sender.sent_messages))
    
    msg = sender.sent_messages[0]
    self.assertEqual(instance_index, msg.instance_index)
    self.assertEqual(HealthClientOpcodes.FAULT_TEST_UNACKNOWLEDGED, msg.mesh_opcode)

    mesh_command = bytearray()
    mesh_command += int(test_id).to_bytes(1, byteorder='little')
    mesh_command += int(company_id, 16).to_bytes(2, byteorder='little')
    self.assertEqual(bytes(mesh_command), msg.mesh_command)

  def test_should_send_period_get_when_send_period_get_method_is_called(self):
    # GIVEN
    sender = BufferedSender()
    instance_index = any_instance_index()

    hc = HealthClient(sender, instance_index)

    # WHEN
    hc.send_period_get()

    # THEN
    self.assertEqual(1, len(sender.sent_messages))
    
    msg = sender.sent_messages[0]
    self.assertEqual(instance_index, msg.instance_index)
    self.assertEqual(HealthClientOpcodes.PERIOD_GET, msg.mesh_opcode)
    self.assertEqual(bytes(), msg.mesh_command)

  def test_should_send_period_set_ack_when_send_period_set_method_is_called_with_unack_set_to_false(self):
    # GIVEN
    sender = BufferedSender()
    instance_index = any_instance_index()

    hc = HealthClient(sender, instance_index)

    fast_period_divider = any_fast_period_divider()

    # WHEN
    hc.send_period_set(fast_period_divider, False)

    # THEN
    self.assertEqual(1, len(sender.sent_messages))
    
    msg = sender.sent_messages[0]
    self.assertEqual(instance_index, msg.instance_index)
    self.assertEqual(HealthClientOpcodes.PERIOD_SET, msg.mesh_opcode)
    self.assertEqual(int(fast_period_divider).to_bytes(1, byteorder='little'), msg.mesh_command)

  def test_should_send_period_set_ack_when_send_period_set_method_is_called_with_unack_set_to_true(self):
    # GIVEN
    sender = BufferedSender()
    instance_index = any_instance_index()

    hc = HealthClient(sender, instance_index)

    fast_period_divider = any_fast_period_divider()

    # WHEN
    hc.send_period_set(fast_period_divider, True)

    # THEN
    self.assertEqual(1, len(sender.sent_messages))
    
    msg = sender.sent_messages[0]
    self.assertEqual(instance_index, msg.instance_index)
    self.assertEqual(HealthClientOpcodes.PERIOD_SET_UNACKNOWLEDGED, msg.mesh_opcode)
    self.assertEqual(int(fast_period_divider).to_bytes(1, byteorder='little'), msg.mesh_command)


if __name__ == "__main__":
  unittest.main()
