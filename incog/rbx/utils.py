from script_context import LuaState, ExtraSpace
from base_script import ProtectedString
from luau import Luau
from init.builder import get_modules

luau_compile = Luau.compile

class Utils:
    @staticmethod
    def get_extraspaces(state: LuaState):
        extraspace_list: list[ExtraSpace] = []

        next_extraspace: ExtraSpace = state.extra_space
        while next_extraspace is not None:
            extraspace_list.append(next_extraspace)
            next_extraspace = next_extraspace.next

        return extraspace_list
    
    @staticmethod
    def to_embedded_code(source: str) -> ProtectedString:
        return ProtectedString(luau_compile(source))
    
    @staticmethod
    def build_initscript() -> str:
        with open("init/loader.luau", "rb") as f:
            loader_script: str = f.read().decode("utf-8", "ignore")

        for module in get_modules():
            module_name: str = module[0]
            module_path: str = module[1]

            with open(module_path, "rb") as f:
                module_content: str = "\n\t\t".join(f.read().decode("utf-8", "ignore").splitlines())
                loader_script = loader_script.replace("--..::Module::..--", f"\t[\"{module_name}\"] = function()\n\t\t{module_content}\n\tend,\n--..::Module::..--")

        loader_script = loader_script.replace("\n--..::Module::..--", "")

        with open("init/full_init.luau", "wb") as f:
            f.write(loader_script.encode("utf-8", "ignore"))

        return loader_script