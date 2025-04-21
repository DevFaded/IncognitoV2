from rbx import RBX
from instance import Instance
from offsets import *
from script_context import WeakThreadRef

rbx_process = RBX.process
rbx_string = RBX.string

is_address_valid = rbx_process.is_address_valid
read_ull = rbx_process.read_ull
write_ull = rbx_process.write_ull

class BindableEvent(Instance):
    def __init__(self, value: Instance | int):
        if isinstance(value, Instance):
            value = value.address

        super().__init__(value)

    @property
    def first(self) -> "Connection":
        events_address: int = read_ull(self.address + BNDABLEVT_EVTS)
        first_address: int = read_ull(events_address + EVNTCONN_FIRST)

        return Connection(first_address) if is_address_valid(first_address) else None

    @property
    def event_count(self) -> int:
        return read_ull(self.address + EVNTCONN_COUNT) - 1 # return true count

    @property
    def event_connections(self) -> list["Connection"]:
        connections: list["Connection"] = []

        current_connection: Connection = self.first
        for _ in range(self.event_count):
            if current_connection is None:
                break
            
            connections.append(current_connection)
            current_connection = current_connection.next

        return connections

class Connection:
    def __init__(self, address: int):
        self.address = address

    @property
    def next(self) -> "Connection":
        next_address: int = read_ull(self.address + CONN_NEXT)
        return Connection(next_address) if is_address_valid(next_address) else None
    
    @property
    def previous(self) -> "Connection":
        previous_address: int = read_ull(self.address + CONN_PREVIOUS)
        return Connection(previous_address) if is_address_valid(previous_address) else None

    @property
    def impl(self) -> "FunctionScriptSlotImpl":
        impl_address: int = read_ull(self.address + CONN_FUNCSCPTSLOT)
        return FunctionScriptSlotImpl(impl_address) if is_address_valid(impl_address) else None

class FunctionScriptSlotImpl:
    def __init__(self, address: int):
        self.address = address

    @property
    def root(self) -> int:
        return read_ull(self.address + FUNCSCPTSLOT_ROOT)
    
    @property
    def name(self) -> str:
        return rbx_string(read_ull(self.address + FUNCSCPTSLOT_NAME))
    
    @property
    def thread_ref(self) -> WeakThreadRef:
        ref_address: int = read_ull(self.address + FUNCSCPTSLOT_THRDREF)
        return WeakThreadRef(ref_address) if is_address_valid(ref_address) else None
    
    @property
    def func_address(self) -> int:
        return read_ull(self.address + FUNCSCPTSLOT_FUNC)
    
    @func_address.setter
    def func_address(self, value: int):
        write_ull(self.address + FUNCSCPTSLOT_FUNC, value)