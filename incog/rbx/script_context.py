from rbx import RBX
from instance import Instance
from offsets import *

rbx_process = RBX.process

is_address_valid = rbx_process.is_address_valid
read_ull = rbx_process.read_ull
read_ul = rbx_process.read_ul
write_ull = rbx_process.write_ull
write_ul = rbx_process.write_ul

class ScriptContext(Instance):
    def __init__(self, value: Instance | int):
        if isinstance(value, Instance):
            value = value.address

        super().__init__(value)

    @property
    def is_game(self) -> bool:
        return self.findfirst_child("LuaAppStarterScript") is None

    def get_global_state(self, index: int = 0) -> "GlobalState":
        global_state_address: int = self.address + (SCNTXT_GLOBALSTATE + (0x140 * index))
        return GlobalState(read_ull(global_state_address))
    
    def set_maxcaps(self, index: int, value: int):
        maxcaps_ptr: int = read_ull(self.address + SCNTXT_MAXCAPS)
        maxcaps_index: int = read_ull(maxcaps_ptr + (0x8 * index))

        write_ull(maxcaps_index + 0x10, CAPABILITIES_ENC ^ value)
        write_ull(maxcaps_index + 0x18, CAPABILITIES_ENC ^ value)

    def set_allownonrbxscripts(self, value: bool):
        write_ul(self.address + SCNTXT_ALWNRBXSCPTS, int(value))
    
class GlobalState:
    def __init__(self, address: int):
        self.address = address

    @property
    def state(self) -> "LuaState":
        return LuaState(read_ull(self.address + 0x8))

class LuaState:
    def __init__(self, address: int):
        self.address = address

    @property
    def top(self) -> int:
        return read_ull(self.address + 0x10)

    @property
    def extra_space(self) -> "ExtraSpace":
        extra_space_address: int = read_ull(self.address + LSTATE_EXTRASPACE)
        return ExtraSpace(extra_space_address) if is_address_valid(extra_space_address) else None
    
class ExtraSpace:
    def __init__(self, address: int):
        self.address = address

    @property
    def next(self) -> "ExtraSpace":
        next_address: int = read_ull(self.address + ESPACE_NEXT)
        return ExtraSpace(next_address) if is_address_valid(next_address) else None
    
    @property
    def thread_count(self) -> int:
        shared_address: int = read_ull(self.address + ESPACE_SHARED)
        return read_ul(shared_address)
    
    @property
    def node(self) -> "WeakThreadRefNode":
        node_address: int = read_ull(self.address + WTHRDREF_NODE)
        return WeakThreadRefNode(node_address) if is_address_valid(node_address) else None

    @property
    def identity(self) -> int:
        return read_ul(self.address + ESPACE_IDENTITY)
    
    @identity.setter
    def identity(self, new_identity: int):
        write_ul(self.address + ESPACE_IDENTITY, new_identity)

    @property
    def capabilities(self) -> int:
        return read_ull(self.address + ESPACE_CAPABILITIES) ^ CAPABILITIES_ENC
    
    @capabilities.setter
    def capabilities(self, new_capabilities: int):
        write_ull(self.address + ESPACE_CAPABILITIES, CAPABILITIES_ENC ^ new_capabilities)

    @property
    def script(self) -> Instance | None:
        script_address: int = read_ull(self.address + ESPACE_SCRIPT)
        return Instance(script_address) if is_address_valid(script_address) else None
    
class WeakThreadRef: # this contains FunctionScriptSlotImpl which is a RbxScriptConnection and we can use it for getconnections
    def __init__(self, address: int):
        self.address = address

    @property
    def previous(self) -> "WeakThreadRef":
        previous_address: int = read_ull(self.address + WTHRDREF_PREVIOUS)
        return WeakThreadRef(previous_address) if is_address_valid(previous_address) else None
    
    @property
    def next(self) -> "WeakThreadRef":
        next_address: int = read_ull(self.address + WTHRDREF_NEXT)
        return WeakThreadRef(next_address) if is_address_valid(next_address) else None
    
    @property
    def live_thread_ref(self) -> "LiveThreadRef":
        live_thread_address: int = read_ull(self.address + WTHRDREF_LTHRDREF)
        return LiveThreadRef(live_thread_address) if is_address_valid(live_thread_address) else None

    @property
    def node(self) -> "WeakThreadRefNode":
        node_address: int = read_ull(self.address + WTHRDREF_NODE)
        return WeakThreadRefNode(node_address) if is_address_valid(node_address) else None
    
    @property
    def lua_state(self):
        return self.live_thread_ref.thread

class WeakThreadRefNode:
    def __init__(self, address: int):
        self.address = address

    @property
    def first(self) -> WeakThreadRef:
        first_address: int = read_ull(self.address + WTHRDREFNODE_FIRST)
        return WeakThreadRef(first_address) if is_address_valid(first_address) else None
    
class LiveThreadRef:
    def __init__(self, address: int):
        self.address = address

    @property
    def thread(self) -> LuaState:
        thread_address: int = read_ull(self.address + LTHRDREF_THREAD)
        return LuaState(thread_address) if is_address_valid(thread_address) else None