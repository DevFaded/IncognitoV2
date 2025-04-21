import re
import ctypes
from ctypes.wintypes import WPARAM, LPARAM
from win32con import *

windll = ctypes.windll

kernel32: ctypes.CDLL = windll.kernel32
user32: ctypes.CDLL = windll.user32
ntdll: ctypes.CDLL = windll.ntdll

class MEMORY_BASIC_INFORMATION64(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_ulonglong),
        ("AllocationBase", ctypes.c_ulonglong),
        ("AllocationProtect", ctypes.c_ulong),
        ("RegionSize", ctypes.c_ulonglong),
        ("State", ctypes.c_ulong),
        ("Protect", ctypes.c_ulong),
        ("Type", ctypes.c_ulong),
    ]

FindWindow = user32.FindWindowW
FindWindow.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
FindWindow.restype = ctypes.c_void_p

IsWindowVisible = user32.IsWindowVisible
IsWindowVisible.argtypes = [ctypes.c_void_p]
IsWindowVisible.restype = ctypes.c_bool

IsWindow = user32.IsWindow
IsWindow.argtypes = [ctypes.c_void_p]
IsWindow.restype = ctypes.c_bool

MessageBox = user32.MessageBoxW
MessageBox.argtypes = [
    ctypes.c_void_p, ctypes.c_wchar_p, 
    ctypes.c_wchar_p, ctypes.c_uint
]; MessageBox.restype = ctypes.c_int

GetForegroundWindow = user32.GetForegroundWindow
GetForegroundWindow.restype = ctypes.c_void_p

GetWindowTextLength = user32.GetWindowTextLengthW
GetWindowTextLength.argtypes = [ctypes.c_void_p]
GetWindowTextLength.restype = ctypes.c_int

GetWindowText = user32.GetWindowTextW
GetWindowText.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_int]
GetWindowText.restype = ctypes.c_bool

SetWindowText = user32.SetWindowTextW
SetWindowText.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p]
SetWindowText.restype = ctypes.c_int

SendMessage = user32.SendMessageW
SendMessage.argtypes = [ctypes.c_void_p, ctypes.c_uint, WPARAM, LPARAM]
SendMessage.restype = LPARAM

GetWindowThreadProcessId = user32.GetWindowThreadProcessId
GetWindowThreadProcessId.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
GetWindowThreadProcessId.restype = ctypes.c_ulong

OpenProcess = kernel32.OpenProcess
OpenProcess.restype = ctypes.c_void_p

VirtualQueryEx = kernel32.VirtualQueryEx
VirtualQueryEx.argtypes = [
     ctypes.c_void_p,
    ctypes.c_void_p,
    ctypes.POINTER(MEMORY_BASIC_INFORMATION64),
    ctypes.c_ulong
]; VirtualQueryEx.restype = ctypes.c_size_t

VirtualAllocEx = kernel32.VirtualAllocEx
VirtualAllocEx.argtypes = [
    ctypes.c_void_p, ctypes.c_void_p,
    ctypes.c_ulonglong, ctypes.c_ulong,
    ctypes.c_ulong
]; VirtualAllocEx.restype = ctypes.c_void_p

NtReadVirtualMemory = ntdll.NtReadVirtualMemory
NtReadVirtualMemory.argtypes = [
    ctypes.c_void_p, ctypes.c_void_p,
    ctypes.c_void_p, ctypes.c_ulong,
    ctypes.POINTER(ctypes.c_ulonglong)
]; NtReadVirtualMemory.restype = ctypes.c_long

NtWriteVirtualMemory = ntdll.NtWriteVirtualMemory
NtWriteVirtualMemory.argtypes = [
    ctypes.c_void_p, ctypes.c_void_p,
    ctypes.c_void_p, ctypes.c_ulong,
    ctypes.POINTER(ctypes.c_ulonglong)
]; NtWriteVirtualMemory.restype = ctypes.c_long