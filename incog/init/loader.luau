local core_packages = game:GetService("CorePackages")

local init_script = Instance.new("ObjectValue")
init_script.Name = "Initialized"; init_script.Value = script
init_script.Parent = core_packages

local load_module
local embedded_modules = {
--..::Module::..--
}; local loaded_modules = {}

function load_module(module_name)
    assert(embedded_modules[module_name], `Module '{module_name}' not found.`)

    local module = loaded_modules[module_name]
    if not module then
        module = embedded_modules[module_name]()
        loaded_modules[module_name] = module
    end

    return module
end

task.spawn(load_module, "init")

local script_name = script.Name
if script_name == "Lumberyak" then
    return require(core_packages.Packages._Index["lumberyak"]["lumberyak"])
elseif script_name == "JestGlobals" then
    local input_manager = Instance.new("VirtualInputManager")
    local escape_key = Enum.KeyCode.Escape

    input_manager:SendKeyEvent(true, escape_key, false, game)
    input_manager:SendKeyEvent(false, escape_key, false, game)
    input_manager:Destroy()

    task.wait(9e9) -- fucks the `dont show again` prompt so it wont close roblox if its enabled
    return {HideTemp = function() end}
end