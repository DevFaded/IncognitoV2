from incog.rbx import RBX
from incog.exploit import Exploit, Bridge
import incog.callbacks.scripts as scripts
import incog.callbacks.misc as misc
import incog.callbacks.filesystem as filesystem

Incognito: Exploit = Exploit()
Ic_Bridge: Bridge = Exploit.bridge

if __name__ == "__main__":
    if RBX.is_roblox_open():
        Ic_Bridge.register_library(scripts)
        Ic_Bridge.register_library(misc)
        Ic_Bridge.register_library(filesystem)

        Incognito.inject()
        Incognito.run_bridge()
    else:
        print("Roblox process not found.")