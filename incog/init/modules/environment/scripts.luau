local bridge = load_module("bridge")
local utils = load_module("utils")

local bridge_post = bridge.post
local fetch_stub = utils.fetch_stub
local c_assert = utils.c_assert

local function _create_thread_holder(): BindableEvent
    local thread_holder = Instance.new("BindableEvent")
    thread_holder.Parent = script; thread_holder.Event:Connect(debug.info(1, "f"))

    return thread_holder
end

local function _scan_env(tbl: table): {any}
    for i, v in next, tbl do
        if typeof(v) == "table" then
            return _scan_env(v)
        elseif typeof(v) == "function" then
            return getfenv(v)
        elseif typeof(v) == "thread" then
            return getfenv(debug.info(v, 1, "f"))
        end
    end
end

local scripts = {}

function scripts.getgenv(): {any}
    -- Temporary
    return getfenv(0)
end

local renv
function scripts.getrenv(): {any}
    if not renv then
        local loader = game:FindFirstChildWhichIsA("LocalScript", true):Clone()
        local holder = fetch_stub()

        loader.Parent = script
        holder.Name = "Holder"; holder.Parent = loader

        local is_success, response = bridge_post("getrenv", {loader, holder})
        if is_success and response then
            loader.Enabled = false; loader.Enabled = true

            renv = getfenv(require(holder))
            renv._G = {}; renv.shared = {}; renv.script = nil
            loader:Destroy(); holder:Destroy()
        end
    end

    return renv
end

function scripts.getsenv(scr: ModuleScript): {any}
    -- Only works for ModuleScripts atm.

    c_assert(typeof(scr) == "Instance", 1, {"Instance"})
    c_assert(scr.ClassName == "ModuleScript", 1, {"ModuleScript"})

    local is_required, constants = pcall(require, scr)
    assert(is_required, `Failed to get script environment for '{scr.Name}`, 0)

    return _scan_env(constants) or {}
end

function scripts.gettenv(thr: thread): {any}
    c_assert(typeof(thr) == "thread", 1, {"thread"})
    return getfenv(debug.info(thr, 1, "f"))
end

function scripts.getscriptfromthread(thr: thread): LocalScript | ModuleScript
    c_assert(typeof(thr) == "thread", 1, {"thread"})
    return rawget(getfenv(debug.info(thr, 1, "f")), "script")
end

function scripts.getloadedmodules(): {ModuleScript}

end

function scripts.getrunningscripts(): {LocalScript | ModuleScript}
    local running_scripts = {}
    local last_script

    local scripts_holder = Instance.new("Folder")
    local fetched_scripts_count = Instance.new("NumberValue")

    scripts_holder.Parent = script
    fetched_scripts_count.Value = 0; fetched_scripts_count.Parent = script

    spawn(function()
        while task.wait() do
            local fetched_scripts = fetched_scripts_count.Value
            if fetched_scripts > 0 then
                for i = 1, fetched_scripts do
                    local script_holder = Instance.new("ObjectValue")
                    script_holder.Value = script; script_holder.Parent = scripts_holder
                end

                fetched_scripts_count.Value = 0
                break
            end
        end
    end)

    local is_success, response = bridge_post("getrunningscripts", {scripts_holder, fetched_scripts_count})
    if is_success and response then
        for i, v in next, scripts_holder:GetChildren() do
            table.insert(running_scripts, v.Value)
        end

        scripts_holder:Destroy()
        fetched_scripts_count:Destroy()
    end

    return running_scripts
end

local script_types = {"LocalScript", "ModuleScript"}
function scripts.getscriptbytecode(scr: LocalScript | ModuleScript): string
    c_assert(typeof(scr) == "Instance", 1, {"Instance"})
    c_assert(table.find(script_types, scr.ClassName), 1, {"LocalScript", "ModuleScript"})

    local is_success, response = bridge_post("getscriptbytecode", {scr})
    return response
end

local cached_closures = {}
function scripts.getscriptclosure(scr: ModuleScript)
    c_assert(typeof(scr) == "Instance", 1, {"Instance"})
    c_assert(table.find(script_types, scr.ClassName), 1, {"LocalScript", "ModuleScript"})

    local script_closure = cached_closures[scr]
    if not script_closure then
        function script_closure()
            return table.clone(require(scr))
        end; cached_closures[scr] = script_closure
    end

    return script_closure
end; scripts.getscriptfunction = scripts.getscriptclosure

function scripts.getscripthash(scr: LocalScript | ModuleScript): string
    c_assert(typeof(scr) == "Instance", 1, {"Instance"})
    c_assert(table.find(script_types, scr.ClassName), 1, {"LocalScript", "ModuleScript"})

    local hash_holder = Instance.new("Script")
    hash_holder.Source = scr.Source

    local hash = hash_holder:GetHash(); hash_holder:Destroy()
    return hash
end

function scripts.dumpstring(source: string): string
    c_assert(typeof(source) == "string", 1, {"string"})
    assert(#source > 1, "Argument #1 must not be empty.")

    local is_success, response = bridge_post("dumpstring", {source})
    return response
end

--[[
function scripts.setthreadidentity(identity: number)
    c_assert(typeof(identity) == "number", 1, {"number"})

    local thread_holder = _create_thread_holder()
    bridge_post("setthreadidentity", {thread_holder, identity})
    thread_holder:Destroy()
end

function scripts.getthreadidentity(): number
    local thread_holder = _create_thread_holder()
    return bridge_post("getthreadidentity", {thread_holder})
end

function scripts.setthreadcapabilities(capabilities: number)
    c_assert(typeof(identity) == "number", 1, {"number"})

    local thread_holder = _create_thread_holder()
    bridge_post("setthreadcapabilities", {thread_holder, capabilities})
    thread_holder:Destroy()
end

function scripts.getthreadcapabilities(): number
    local thread_holder = _create_thread_holder()
    bridge_post("getthreadcapabilities", {thread_holder})
    thread_holder:Destroy()
end]] -- will fix

return scripts