from imports import *

current_window: ctypes.c_void_p = GetForegroundWindow()

def get_current_window_text() -> str:
    windowLength: int = GetWindowTextLength(current_window) + 1
    buffer = ctypes.create_unicode_buffer(windowLength)
    GetWindowText(current_window, buffer, windowLength)
    return buffer.value

class MemEx:
    def _find_window(window_title: str) -> ctypes.c_void_p:
        return FindWindow(None, window_title)
    
    def _set_window(self, window: ctypes.c_void_p) -> None:
        self.window = window

    def _close_window(self):
        if "window" in self.__dict__ and self.window is not None:
            SendMessage(self.window, WM_CLOSE, 0, 0)

    def _message_box(self, caption: str, text: str, message_box_type: int = 0) -> int:
        return MessageBox(self.window, text, caption, message_box_type)
    
    def _get_process_id(window: ctypes.c_void_p) -> int:
        process_id = ctypes.c_ulong()
        GetWindowThreadProcessId(window, ctypes.byref(process_id))
        return process_id.value

    def __init__(self, process_id: int):
        self.window = None
        self.process_id = process_id
        self.process_handle = OpenProcess(PROCESS_ALL_ACCESS, False, process_id)

    @staticmethod
    def is_address_valid(address: int) -> bool:
        return address > 1000 and address < 0x7FFFFFFF0000
    
    def virtual_query(self, address: int) -> MEMORY_BASIC_INFORMATION64:
        memory_basic_info = MEMORY_BASIC_INFORMATION64()

        VirtualQueryEx(
            self.process_handle,
            ctypes.c_void_p(address),
            ctypes.byref(memory_basic_info),
            ctypes.sizeof(memory_basic_info)
        )

        return memory_basic_info
    
    def allocate_memory(self, address: int, size: int) -> int:
        return VirtualAllocEx(
            self.process_handle,
            ctypes.c_void_p(address),
            size,
            MEM_COMMIT | MEM_RESERVE,
            PAGE_READWRITE
        )

    def read_buffer(self, buffer, address: int) -> bool:
        return NtReadVirtualMemory(
            self.process_handle,
            ctypes.c_void_p(address),
            ctypes.byref(buffer),
            ctypes.sizeof(buffer),
            None
        )

    def read(self, c_type, address: int):
        c_buffer = c_type()
        self.read_buffer(c_buffer, address)
        return c_buffer.value
    
    def read_ul(self, address: int) -> int:
        return self.read(ctypes.c_ulong, address)
    
    def read_ull(self, address: int) -> int:
        return self.read(ctypes.c_ulonglong, address)
    
    def read_float(self, address: int) -> float:
        return self.read(ctypes.c_float, address)
    
    def read_double(self, address: int) -> float:
        return self.read(ctypes.c_double, address)
    
    def read_string(self, address: int, size: int = 100) -> str:
        c_buffer = (size * ctypes.c_char)()
        self.read_buffer(c_buffer, address)
        return c_buffer.value.decode("utf-8", "ignore")
    
    def read_byte(self, address: int) -> int:
        c_buffer = ctypes.c_byte()
        self.read_buffer(c_buffer, address)
        return c_buffer.value
    
    def read_bytes(self, address: int, size: int = 100) -> bytes:
        c_buffer = (size * ctypes.c_char)()
        self.read_buffer(c_buffer, address)
        return c_buffer.raw
    
    def write_buffer(self, address: int, buffer) -> bool:
        return NtWriteVirtualMemory(
            self.process_handle,
            ctypes.c_void_p(address),
            ctypes.byref(buffer),
            ctypes.sizeof(buffer),
            None
        )
    
    def write(self, c_type, address: int, value):
        c_buffer = c_type(value)
        self.write_buffer(address, c_buffer)

    def write_ul(self, address: int, value: int):
        c_buffer = ctypes.c_ulong(value)
        self.write_buffer(address, c_buffer)

    def write_ull(self, address: int, value: int):
        c_buffer = ctypes.c_ulonglong(value)
        self.write_buffer(address, c_buffer)

    def write_float(self, address: int, value: float):
        c_buffer = ctypes.c_float(value)
        self.write_buffer(address, c_buffer)

    def write_double(self, address: int, value: float):
        c_buffer = ctypes.c_double(value)
        self.write_buffer(address, c_buffer)

    def write_string(self, address: int, value: str):
        self.write_bytes(
            address, 
            value.encode("utf-8", "ignore") + b'\x00'
        )

    def write_byte(self, address: int, value: int):
        c_buffer = ctypes.c_byte(value)
        self.write_buffer(address, c_buffer)

    def write_bytes(self, address: int, value: bytes):
        c_buffer = (len(value) * ctypes.c_char)(*value)
        self.write_buffer(address, c_buffer)

    def pattern_scan(self, pattern: bytes):
        region = 0

        while region < 0x7FFFFFFF0000:
            mbi = self.virtual_query(region)

            region_size: int = mbi.RegionSize
            protection: int = mbi.Protect

            is_safe: bool = (mbi.State & MEM_COMMIT) and not (region_size == 0x200000 and protection == PAGE_READWRITE)
            is_readable: bool = protection

            if is_safe and is_readable:
                current_bytes = self.read_bytes(region, mbi.RegionSize)

                match = re.search(pattern, current_bytes, re.DOTALL)

                if match:
                    return region + match.span()[0]

            region += mbi.RegionSize

        return 0
	