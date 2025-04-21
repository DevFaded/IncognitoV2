from rbx import RBX
from instance import Instance
from luau import Luau
from offsets import *

rbx_process = RBX.process

is_address_valid = rbx_process.is_address_valid
allocate_memory = rbx_process.allocate_memory
read_ull = rbx_process.read_ull
read_ul = rbx_process.read_ul
read_bytes = rbx_process.read_bytes
write_ull = rbx_process.write_ull
write_bytes = rbx_process.write_bytes

luau_compile = Luau.compile
luau_compress = Luau.compress

class ProtectedString:
    def __init__(self, bytecode: bytes):
        self.bytecode = bytecode
        self.size = len(bytecode)

class BaseScript(Instance):
    @staticmethod
    def _get_bytecode_pointers(address: int) -> tuple[int, int]:
        embedded_code_ptr: int = read_ull(address)
        return embedded_code_ptr, read_ull(embedded_code_ptr + EMBDC_BYTECODE)
    
    @staticmethod
    def _get_embedded_code(address: int) -> ProtectedString | None:
        embedded_code_ptr, bytecode_ptr = BaseScript._get_bytecode_pointers(address)
        
        return ProtectedString(
            read_bytes(
                bytecode_ptr, 
                read_ull(embedded_code_ptr + EMBDC_BYTECODESIZE)
            ))
    
    @staticmethod
    def _set_embedded_code(address: int, value: ProtectedString):
        compressed_value: bytes = luau_compress(value.bytecode)
        compressed_size: int = len(compressed_value)

        embedded_code_ptr, bytecode_ptr = BaseScript._get_bytecode_pointers(address)
        bytecode_ptr: int = allocate_memory(None, compressed_size)

        write_bytes(bytecode_ptr, compressed_value)
        write_ull(embedded_code_ptr + EMBDC_BYTECODE, bytecode_ptr)
        write_ull(embedded_code_ptr + EMBDC_BYTECODESIZE, compressed_size)

    def __init__(self, value: Instance | int):
        if isinstance(value, Instance):
            value = value.address

        super().__init__(value)