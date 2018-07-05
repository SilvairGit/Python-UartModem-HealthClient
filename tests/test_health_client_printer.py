import random
import unittest
import binascii
import re

from silvair_health_client.health_client_printer import HealthClientStatusPrinter


def any_attention_s():
  return random.getrandbits(8)


def any_company_id():
  return random.getrandbits(16)


def any_test_id():
  return random.getrandbits(8)


def any_fast_period_divider():
  return random.randrange(0, 15)


class BufferedConsoleOut:

  def __init__(self):
    self._messages = []

  def print_standard_message(self, msg):
    self._messages.append(msg)

  @property
  def messages(self):
    return self._messages


class TestHealthClientPrinter(unittest.TestCase):

  def test_should_print_attention_status_when_print_attention_status_method_is_called(self):
    # GIVEN
    console_out = BufferedConsoleOut()
    printer = HealthClientStatusPrinter(console_out)

    attention_s = any_attention_s()

    mesh_command = int(attention_s).to_bytes(1, byteorder="little")

    # WHEN
    printer.print_attention_status(mesh_command)

    # THEN
    self.assertEqual(1, len(console_out.messages))

    msg_re = re.compile(r"Attention:\s(\d+)\s\[s\]")
    msg_match = msg_re.match(console_out.messages[0])

    self.assertTrue(msg_match is not None)
    self.assertEqual(attention_s, int(msg_match.group(1)))


  def test_should_print_period_status_when_print_period_status_method_is_called(self):
    # GIVEN
    console_out = BufferedConsoleOut()
    printer = HealthClientStatusPrinter(console_out)

    fast_period_divider = any_fast_period_divider()

    mesh_command = int(fast_period_divider).to_bytes(1, byteorder="little")

    # WHEN
    printer.print_period_status(mesh_command)

    # THEN
    self.assertEqual(1, len(console_out.messages))

    msg_re = re.compile(r"Fast Period Divider:\s(\d+)\s\(value\s2\^n:\s(\d+)\)")
    msg_match = msg_re.match(console_out.messages[0])

    self.assertTrue(msg_match is not None)
    self.assertEqual(fast_period_divider, int(msg_match.group(1)))
    self.assertEqual(1 << fast_period_divider, int(msg_match.group(2)))

  def test_should_print_current_status_when_print_current_status_method_is_called(self):
    # GIVEN
    console_out = BufferedConsoleOut()
    printer = HealthClientStatusPrinter(console_out)

    test_id = any_test_id()
    company_id = any_company_id()

    mesh_command = bytearray()
    mesh_command += int(test_id).to_bytes(1, byteorder="little")
    mesh_command += int(company_id).to_bytes(2, byteorder="little")

    # WHEN
    printer.print_current_status(mesh_command)

    # THEN
    self.assertEqual(1, len(console_out.messages))

    msg_re = re.compile(r"Current Status:\s+src_addr:\s(0x\w+),\s+test_id:\s(\d+),\s+company_id:\s(0x\w+),\s+faults:\s\[(.*)\]")
    msg_match = msg_re.match(console_out.messages[0])

    self.assertTrue(msg_match is not None)

  def test_should_print_fault_status_when_print_fault_status_method_is_called(self):
    # GIVEN
    console_out = BufferedConsoleOut()
    printer = HealthClientStatusPrinter(console_out)

    test_id = any_test_id()
    company_id = any_company_id()

    mesh_command = bytearray()
    mesh_command += int(test_id).to_bytes(1, byteorder="little")
    mesh_command += int(company_id).to_bytes(2, byteorder="little")

    # WHEN
    printer.print_fault_status(mesh_command)

    # THEN
    self.assertEqual(1, len(console_out.messages))

    msg_re = re.compile(r"Fault Status:\s+src_addr:\s(0x\w+),\s+test_id:\s(\d+),\s+company_id:\s(0x\w+),\s+faults:\s\[(.*)\]")
    msg_match = msg_re.match(console_out.messages[0])

    self.assertTrue(msg_match is not None)


if __name__ == "__main__":
  unittest.main()
