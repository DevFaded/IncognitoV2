from rbx import RBX
from offsets import *

rbx_process = RBX.process
rbx_string = RBX.string

read_ull = rbx_process.read_ull
read_ul = rbx_process.read_ul
write_ul = rbx_process.write_ul

_get_children_addresses = RBX._get_children_addresses

class ClassDescriptor:
    @staticmethod
    def _get_children(address: int, children_type) -> list:
        child_list: list = []
        child_begin, child_end = _get_children_addresses(address)

        for i in range(child_begin, child_end, 0x8):
            child_instance = children_type(read_ull(i))
            child_list.append(child_instance)

        return child_list

    def __init__(self, address: int):
        self.address = address

    @property
    def name(self) -> str:
        return rbx_string(read_ull(self.address + MDESC_NAME))

    @property
    def security(self) -> int:
        return read_ul(self.address + CDESC_CAPABILITIES)
    
    @security.setter
    def security(self, new_capabilities: int) -> int:
        return write_ul(self.address + CDESC_CAPABILITIES, new_capabilities)

    def get_properties(self) -> list["PropertyDescriptor"]:
        return self._get_children(
            self.address + CDESC_PROPERTIES, PropertyDescriptor)
    
    def get_methods(self) -> list["BoundedFuncDescriptor"]:
        return self._get_children(
            self.address + CDESC_METHODS, BoundedFuncDescriptor)
    
class MemberDescriptor:
    def __init__(self, address: int):
        self.address = address

    @property
    def name(self) -> str:
        return rbx_string(read_ull(self.address + MDESC_NAME))
    
    @property
    def security(self) -> int:
        return read_ul(self.address + MDESC_SECURITY)

    @security.setter
    def security(self, new_security: int):
        write_ul(self.address + MDESC_SECURITY, new_security)
    
class PropertyDescriptor(MemberDescriptor):
    pass

class BoundedFuncDescriptor(MemberDescriptor):
    pass