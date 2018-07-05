import unittest
import random

from silvair_otau_demo.console_out import ConsoleOut
from silvair_health_client.utils import ModelIdToInstanceIndexMapper, HealthClientOpcodesDispatcher


def any_model_id():
  return random.getrandbits(16)


def any_model_id_different_than(model_id):
  mid = any_model_id()

  while mid == model_id:
    mid = any_model_id()

  return mid


def any_models_ids():
  return [any_model_id() for _ in range(random.randrange(0, 100))]


def any_opcode():
  return random.getrandbits(16)


class TestModelIdToInstanceIndexMapper(unittest.TestCase):

  def test_should_map_models_ids_on_instance_indexes_when_map_models_ids_method_is_called(self):
    # GIVEN
    mapper = ModelIdToInstanceIndexMapper(ConsoleOut())
    models_ids = any_models_ids()

    # WHEN
    mapper.map_models_ids(models_ids)

    # THEN
    for i, model_id in enumerate(models_ids):
      self.assertTrue(i+1 in mapper[model_id])

  def test_should_return_true_when_method_contains_model_id_is_called_with_model_id_mapped_into_instance_index(self):
    # GIVEN
    mapper = ModelIdToInstanceIndexMapper(ConsoleOut())
    model_id = any_model_id()

    # WHEN
    mapper.map_models_ids([model_id])

    # THEN
    self.assertTrue(mapper.contains_model_id(model_id))

  def test_should_return_false_when_method_contains_model_id_is_called_with_model_id_not_mapped_into_instance_index(self):
    # GIVEN
    mapper = ModelIdToInstanceIndexMapper(ConsoleOut())
    model_id = any_model_id()

    # WHEN
    mapper.map_models_ids([model_id])

    # THEN
    self.assertFalse(mapper.contains_model_id(any_model_id_different_than(model_id)))

  def test_should_return_false_when_method_contains_model_id_is_called_with_no_mapped_models_ids(self):
    # GIVEN
    mapper = ModelIdToInstanceIndexMapper(ConsoleOut())

    # THEN
    self.assertFalse(mapper.contains_model_id(any_model_id()))


class TestHealthClientOpcodesDispatcher(unittest.TestCase):

  def test_should_return_true_when_dispatch_method_is_called_with_opcode_mapped_during_initialization(self):
    # GIVEN
    def test_func(command):
      pass

    opcode = any_opcode()
    mapping = {opcode: test_func}

    dispatcher = HealthClientOpcodesDispatcher(mapping)

    # WHEN
    res = dispatcher.dispatch(opcode, bytes())

    # THEN
    self.assertTrue(res)

  def test_should_call_test_func_when_dispatch_method_is_called_with_opcode_mapped_during_initialization(self):
    # GIVEN
    self.test_func_called = False

    def test_func(command):
      self.test_func_called = True

    opcode = any_opcode()
    mapping = {opcode: test_func}

    dispatcher = HealthClientOpcodesDispatcher(mapping)

    # WHEN
    dispatcher.dispatch(opcode, bytes())

    # THEN
    self.assertTrue(self.test_func_called)

  def test_should_return_false_when_dispatch_method_is_called_with_opcode_not_mapped_during_initialization(self):
    # GIVEN
    mapping = {}

    dispatcher = HealthClientOpcodesDispatcher(mapping)

    # WHEN
    res = dispatcher.dispatch(any_opcode(), bytes())

    # THEN
    self.assertFalse(res)


if __name__ == "__main__":
  unittest.main()
