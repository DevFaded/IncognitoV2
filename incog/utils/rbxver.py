from winreg import HKEY_CURRENT_USER, OpenKeyEx, QueryValueEx

robloxPlayer = None

try:
    robloxPlayer = OpenKeyEx(
        HKEY_CURRENT_USER,
        r"SOFTWARE\\ROBLOX Corporation\\Environments\\roblox-player"
    )
except FileNotFoundError:
    exit(1)

ROBLOX_EXE_PATH: str = QueryValueEx(robloxPlayer, "clientExe")[0]
ROBLOX_VERSION_PATH: str = ROBLOX_EXE_PATH.replace(r"\RobloxPlayerBeta.exe", "")
ROBLOX_VERSION: str = QueryValueEx(robloxPlayer, "version")[0]