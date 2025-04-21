from rbx import RBX
from base_script import BaseScript, ProtectedString
from script_context import WeakThreadRefNode
from offsets import *

rbx_process = RBX.process

is_address_valid = rbx_process.is_address_valid
read_ull = rbx_process.read_ull

class LocalScript(BaseScript):
    def __init__(self, value):
        super().__init__(value)

    @property
    def embedded_code(self) -> ProtectedString:
        return self._get_embedded_code(self.address + LSCPT_EMBEDDEDCODE)
    
    @embedded_code.setter
    def embedded_code(self, value: ProtectedString):
        self._set_embedded_code(
            self.address + LSCPT_EMBEDDEDCODE,
            value)
        
    @property
    def thread_node(self) -> WeakThreadRefNode:
        node_address: int = read_ull(self.address + BSCPT_WTHRDREFNODE)
        return WeakThreadRefNode(node_address) if is_address_valid(node_address) else None