from rbx import RBX
from time import sleep
from reflection import ClassDescriptor
from offsets import *

rbx_process = RBX.process
rbx_string = RBX.string

is_address_valid = rbx_process.is_address_valid
read_ull = rbx_process.read_ull
write_ull = rbx_process.write_ull

_get_children_addresses = RBX._get_children_addresses
_get_children_count = RBX._get_children_count
_select_children = RBX._select_children

class Instance:    
    @staticmethod
    def _get_children(child_begin: int, child_end: int, safe: bool = True):
        skip_next: bool = False
        for i in range(_get_children_count(child_begin, child_end)):
            if skip_next and safe:
                skip_next = False
                continue

            child_instance: Instance = Instance(_select_children(child_begin, i))
            if child_instance.class_name == "MarketplaceService" and safe: # no more crash, fuck suspending threads only gay niggers use that
                skip_next = True

            yield child_instance

    def __init__(self, address: int):
        self.address = address
        self.class_descriptor = ClassDescriptor(
            read_ull(self.address + INST_CDESCRIPTOR))
        
    @property
    def self(self) -> "Instance":
        return Instance(read_ull(self.address + INST_SELF))
    
    @self.setter
    def self(self, value: int):
        if isinstance(value, Instance):
            value = value.address

        write_ull(self.address + INST_SELF, value)

    @property
    def class_name(self) -> str:
        return self.class_descriptor.name

    @property
    def name(self) -> str:
        return rbx_string(read_ull(self.address + INST_NAME))
    
    @property
    def parent(self) -> "Instance":
        parent_address: int = read_ull(self.address + INST_PARENT)
        return Instance(parent_address) if is_address_valid(parent_address) else None
    
    @parent.setter
    def parent(self, value: int):
        if isinstance(value, Instance):
            value = value.address

        write_ull(self.address + INST_PARENT, value)
    
    def get_children(self, safe: bool = True) -> list["Instance"]:
        child_list: list["Instance"] = []
        child_begin, child_end = _get_children_addresses(read_ull(self.address + INST_CHILDREN))

        for child_instance in self._get_children(child_begin, child_end):
            child_list.append(child_instance)
            
        return child_list
    
    def select_child(self, index: int) -> "Instance":
        child_begin, _ = _get_children_addresses(read_ull(self.address + INST_CHILDREN))
        return Instance(_select_children(child_begin, index))
    
    def findfirst_child(self, name: str) -> "Instance":
        child_begin, child_end = _get_children_addresses(read_ull(self.address + INST_CHILDREN))

        for child_instance in self._get_children(child_begin, child_end):
            if child_instance.name == name:
                return child_instance
            
    def findfirst_class(self, class_name: str) -> "Instance":
        child_begin, child_end = _get_children_addresses(read_ull(self.address + INST_CHILDREN))

        for child_instance in self._get_children(child_begin, child_end):
            if child_instance.class_name == class_name:
                return child_instance
            
    def waitfor_child(self, name: str, timeout: int = 5) -> "Instance":
        for _ in range(timeout):
            found_child: Instance = self.findfirst_child(name)
            if found_child is not None:
                return found_child
            
            sleep(1)

    def waitfor_class(self, class_name: str, timeout: int = 5) -> "Instance":
        for _ in range(timeout):
            found_child: Instance = self.findfirst_class(class_name)
            if found_child is not None:
                return found_child
            
            sleep(1) 
            
    def __getitem__(self, name: str):
        if type(name) == int:
            return self.select_child(name)
        elif name.endswith("-C"):
            return self.findfirst_class(name.removesuffix("-C"))
        elif name.endswith("-CW"):
            return self.waitfor_class(name.removesuffix("-CW"))

        return self.findfirst_child(name)
    
    def __str__(self):
        return f"{self.name} {hex(self.address)}"