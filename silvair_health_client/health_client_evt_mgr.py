from silvair_otau_demo.console_out import ConsoleOut
from silvair_otau_demo.event_mgr import EventMgr

from silvair_health_client.utils import ModelIdToInstanceIndexMapper, HealthClientOpcodesDispatcher


class HealtClientEventMgr(EventMgr):

    def __init__(self,
                 console_out: ConsoleOut,
                 mid_to_ii_mapper: ModelIdToInstanceIndexMapper,
                 opcodes_disp: HealthClientOpcodesDispatcher):
        super(HealtClientEventMgr, self).__init__(console_out)
        self._mid_to_ii_mapper = mid_to_ii_mapper
        self._opcodes_disp = opcodes_disp

    def uart_registered_models(self, model_ids: list):
        self._mid_to_ii_mapper.map_models_ids(model_ids)
        super().uart_registered_models(model_ids)

    def uart_mesh_request(self, opcode: int, command: bytes):
        if self._opcodes_disp.dispatch(opcode, command):
            return
        
        super().uart_mesh_request(opcode, command)