from rbx import RBX
from instance import Instance
from offsets import *

rbx_process = RBX.process

is_address_valid = rbx_process.is_address_valid
read_ull = rbx_process.read_ull
read_double = rbx_process.read_double
write_ull = rbx_process.write_ull
write_double = rbx_process.write_double

class NumberValue(Instance):
    def __init__(self, value: Instance | int):
        if isinstance(value, Instance):
            value = value.address

        super().__init__(value)

    @property
    def value(self) -> float:
        return read_double(self.address + VALUEBASE_VALUE)
    
    @value.setter
    def value(self, new: float):
        write_double(self.address + VALUEBASE_VALUE, new)