
class ModelIdToInstanceIndexMapper(object):
    """ Model Id to Instance Index mapper. """

    def __init__(self):
        """ Initalize mapper """
        self._mid_to_iid = []
        self._instance_index = 1
    
    def map_models_ids(self, model_ids):
        """ Map model ids on the instance indexes.

        :param  model_ids: list[ModelId], List of model indexes.
        :return            None
        """

        self._instance_index = 1
        
        for model_id in model_ids:
            self._mid_to_iid.append(model_id)
            print("Mapped model_id to instance_index: {:04x} => {}".format(model_id, self._instance_index))

            self._instance_index += 1

    def __getitem__(self, key):
        instance_index = 1
        iids = []

        for model_id in self._mid_to_iid:
            if key == model_id:
                iids.append(instance_index)

            instance_index += 1

        return tuple(iids)

    def contains_model_id(self, model_id):
        """ Check Model Id has been mapped onto instance index. 

        :param model_id: ModelId, Model Id
        :return          bool
        """
        return any([model_id == mid for mid in self._mid_to_iid])


class HealthClientOpcodesDispatcher:
    """ Health Client opcodes dispatcher """
    
    def __init__(self, opcode_to_func_map):
        """ Initialize dispatcher 

        :param opcode_to_func_map: dict<HealthClientOpcodes, Callable>, Health Client Opcode to function.
        :return                    bool, True if opcode has been dispatched, False otherwise
        """
        self._opcode_to_func_map = opcode_to_func_map
        
        
    def dispatch(self, opcode, command):
        """ Dispatch messages """
        result = True

        try:
            func = self._opcode_to_func_map[opcode]
            func(command)

        except KeyError:
            result = False

        return result
