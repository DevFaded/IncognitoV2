local EXECUTOR_INFO = {"Incognito", "V2"}

local bridge = load_module("bridge")
local utils = load_module("utils")

local bridge_post = bridge.post
local c_assert = utils.c_assert

local lz4 = load_module("lz4")

local misc = {}

function misc.identifyexecutor(): (string, string)
    return table.unpack(EXECUTOR_INFO)
end

function misc.getexecutorname(): string
    return EXECUTOR_INFO[1]
end

function misc.lz4compress(data: string): string
    c_assert(typeof(data) == "string", 1, {"string"})
    assert(#data > 0, "Argument #1 must not be empty.")

    return lz4.compress(data)
end

function misc.lz4decompress(data: string): string
    c_assert(typeof(data) == "string", 1, {"string"})
    assert(#data > 0, "Argument #1 must not be empty.")

    return lz4.decompress(data)
end

function misc.messagebox(text: string, caption: string, flags: number): number
    text = text or ''
    caption = caption or EXECUTOR_INFO[1]
    flags = flags or 0

    local is_success, response = bridge_post("messagebox", {text, caption, flags})
    return response
end

function misc.setclipboard(text: string)
    c_assert(typeof(text) == "string", 1, {"string"})
    assert(#data > 0, "Argument #1 must not be empty.")

    bridge_post("setclipboard", {text})
end; misc.toclipboard = misc.setclipboard

return misc