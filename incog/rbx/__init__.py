from memex import MemEx, FindWindow, IsWindow
from render_view import get_render_view
from offsets import *

class RBX:
    window = FindWindow(None, "Roblox")
    process: MemEx = MemEx(MemEx._get_process_id(window))

    @staticmethod
    def is_roblox_open() -> bool:
        return RBX.process.process_id != 0 and IsWindow(RBX.window)

    @staticmethod
    def _get_children_addresses(child_pointer: int) -> tuple[int, int]:
        read_ull = RBX.process.read_ull
        child_begin: int = read_ull(child_pointer)
        child_end: int = read_ull(child_pointer + 0x8)
        return child_begin, child_end

    @staticmethod
    def _get_children_count(child_begin: int, child_end: int, step: int = 0x10) -> int:
        return (child_end - child_begin) // step

    @staticmethod
    def _select_children(child_begin: int, index: int) -> int:
        return RBX.process.read_ull(child_begin + (index * 0x10))
    
    @staticmethod
    def string(address: int) -> str:
        rbx_process = RBX.process
        read_ul = rbx_process.read_ul

        string_length: int = read_ul(address + 0x10)
        string_check: int = read_ul(address + 0x18)

        if string_check > 15:
            address = rbx_process.read_ull(address)

        return rbx_process.read_string(address, string_length)

    @staticmethod
    def get_datamodel() -> int:
        rbx_process = RBX.process
        read_ull = rbx_process.read_ull

        render_view: int = get_render_view(rbx_process)
        datamodel_holder: int = read_ull(render_view + DATAMODEL_HOLDER)
        real_datamodel: int = read_ull(datamodel_holder + REAL_DATAMODEL)

        return real_datamodel