from rbx import RBX
from script_context import GlobalState, WeakThreadRefNode
from base_script import BaseScript, ProtectedString
from offsets import *

rbx_process = RBX.process

is_address_valid = rbx_process.is_address_valid
read_ull = rbx_process.read_ull
read_ul = rbx_process.read_ul

class ModuleScript(BaseScript):
    def __init__(self, value):
        super().__init__(value)

    @property
    def embedded_code(self) -> ProtectedString:
        return self._get_embedded_code(self.address + MSCPT_EMBEDDEDCODE)
    
    @embedded_code.setter
    def embedded_code(self, value: ProtectedString):
        self._set_embedded_code(
            self.address + MSCPT_EMBEDDEDCODE,
            value)
        
    @property
    def per_vm_state(self) -> "PerVMState":
        state_map_ptr: int = read_ull(self.address + MSCPT_VMSTATEMAP)
        return PerVMState(read_ull(state_map_ptr)) if is_address_valid(state_map_ptr) else None
    
# https://github.com/P0L3NARUBA/roblox-2016-source-code/blob/f88642e35d6429875882f7a96a4609b5793ee435/App/include/script/ModuleScript.h#L31
class PerVMState:
    def __init__(self, address: int):
        self.address = address

    @property
    def loading_state(self) -> int:
        return read_ul(self.address + VMSTM_LOADINGSTATE)
    
    @property
    def node(self) -> WeakThreadRefNode:
        node_address: int = read_ull(self.address + VMSTM_WTHRDREFNODE)
        return WeakThreadRefNode(node_address) if is_address_valid(node_address) else None
    
    @property
    def global_state(self) -> GlobalState:
        global_state_address: int = read_ull(self.address + VMSTM_GLOBALSTATE)
        return GlobalState(global_state_address) if is_address_valid(global_state_address) else None