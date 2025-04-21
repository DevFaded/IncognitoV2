from rbx import RBX
from memex.imports import MessageBox
from win32clipboard import OpenClipboard, CloseClipboard, EmptyClipboard, SetClipboardData

rbx_window = RBX.window

def messagebox(data):
    text: str = data[0]
    caption: str = data[1]
    flags: int = data[2]

    return MessageBox(rbx_window, text, caption, flags)

def queue_on_teleport(data):
    pass

def request(data):
    pass

def setclipboard(data):
    text: str = data[0]
    success: bool = False

    try:
        OpenClipboard()
        EmptyClipboard()
        SetClipboardData(13, text)
        success = True
    finally:
        CloseClipboard()

    return success

__library__ = [
    messagebox, queue_on_teleport,
    request, setclipboard
]