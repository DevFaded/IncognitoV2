from rbx.instance import Instance
from rbx.local_script import LocalScript
from rbx.module_script import ModuleScript
from rbx.object_value import ObjectValue
from rbx.number_value import NumberValue
from rbx.bindable_event import BindableEvent
from rbx.script_context import ScriptContext, LuaState, ExtraSpace
from rbx.utils import Utils
from rbx.luau import Luau

from exploit.instances import Instances

luau_compile = Luau.compile
luau_decompress = Luau.decompress
to_embedded_code = Utils.to_embedded_code

def _convert_to_script(instance: Instance) -> LocalScript | ModuleScript:
    script: Instance = instance
    script_class: str = script.class_name

    if script_class == "LocalScript":
        script = LocalScript(script)
    elif script_class == "ModuleScript":
        script = ModuleScript(script)

    return script

def _get_bindable_event_extraspace(bindable_event: BindableEvent) -> ExtraSpace:
    bindable_event: BindableEvent = BindableEvent(bindable_event)
    return bindable_event.first.impl.thread_ref.lua_state.extra_space

def getrenv(data):
    loader: LocalScript = LocalScript(data[0])
    holder: ModuleScript = ModuleScript(data[1])

    loader.embedded_code = to_embedded_code("require(script.Holder)")
    holder.embedded_code = to_embedded_code("return function() end")

    return True

def getrunningscripts(data):
    scripts_holder: ObjectValue = ObjectValue(data[0])
    fetched_scripts_count: NumberValue = NumberValue(data[1])
    script_context: ScriptContext = Instances.script_context

    running_scripts: list["Instance"] = []
    if script_context is not None:
        global_state = script_context.get_global_state(0)
        for extra_space in Utils.get_extraspaces(global_state.state):
            script = extra_space.script
            if script is not None and script.address not in running_scripts:
                running_scripts.append(script.address)

    fetched_scripts_count.value = float(len(running_scripts))

    if len(running_scripts) > 0:
        while fetched_scripts_count.value > 0:
            pass

        for index, holder in enumerate(scripts_holder.get_children()):
            holder: ObjectValue = ObjectValue(holder)
            holder.value = running_scripts[index]

    return True

def getscriptbytecode(data):
    script: LocalScript | ModuleScript = _convert_to_script(data[0])
    script_embedded_code = script.embedded_code

    return "" if script_embedded_code.size < 1 else luau_decompress(
        script_embedded_code.bytecode).decode("utf-8", "ignore")

def dumpstring(data):
    source: str = data[0]
    bytecode: bytes = luau_compile(source)

    return bytecode.decode("utf-8", "ignore")

def setthreadidentity(data):
    extra_space: ExtraSpace = _get_bindable_event_extraspace(data[0])
    extra_space.identity = data[1]

    return True

def getthreadidentity(data) -> int:
    extra_space: ExtraSpace = _get_bindable_event_extraspace(data[0])
    return extra_space.identity

def setthreadcapabilities(data):
    extra_space: ExtraSpace = _get_bindable_event_extraspace(data[0])
    extra_space.capabilities = data[1]

    return True

def getthreadcapabilities(data) -> int:
    extra_space: ExtraSpace = _get_bindable_event_extraspace(data[0])
    return extra_space.capabilities

__library__ = [
    getrenv, getrunningscripts,
    getscriptbytecode, dumpstring, 
    setthreadidentity, getthreadidentity, 
    setthreadcapabilities, getthreadcapabilities
]