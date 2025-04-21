from re import findall
from os import getenv, listdir, remove
from os.path import join, isdir, isfile
from memex import MemEx, MessageBox, get_current_window_text, MB_ICONERROR
from offsets import RENDERJOB_RENDERVIEW

LOCALAPPDATA_PATH = getenv("LOCALAPPDATA")
ROBLOX_LOGS_PATH = join(LOCALAPPDATA_PATH, "Roblox", "logs")

RENDER_VIEW: int = 0

if not isdir(ROBLOX_LOGS_PATH):
    MessageBox(None, "Roblox logs directory not found.", get_current_window_text(), MB_ICONERROR)
    exit(1)

def get_render_view(process: MemEx) -> int:
    global RENDER_VIEW
    if not RENDER_VIEW:
        render_job = process.pattern_scan(b"RenderJob\(EarlyRendering\;")
        RENDER_VIEW = process.read_ull(render_job + RENDERJOB_RENDERVIEW)

    return RENDER_VIEW