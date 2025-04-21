from rbx import RBX
from instance import Instance
from offsets import *

rbx_process = RBX.process

is_address_valid = rbx_process.is_address_valid
read_ull = rbx_process.read_ull
write_ull = rbx_process.write_ull

class ObjectValue(Instance):
    def __init__(self, value: Instance | int):
        if isinstance(value, Instance):
            value = value.address

        super().__init__(value)

    @property
    def value(self) -> Instance:
        value_address: int = read_ull(self.address + VALUEBASE_VALUE)
        return Instance(value_address) if is_address_valid(value_address) else None
    
    @value.setter
    def value(self, new: int):
        if isinstance(new, Instance):
            new = new.address

        write_ull(self.address + VALUEBASE_VALUE, new)