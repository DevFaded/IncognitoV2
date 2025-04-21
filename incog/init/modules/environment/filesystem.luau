local bridge = load_module("bridge")
local utils = load_module("utils")

local bridge_post = bridge.post
local c_assert = utils.c_assert

local function _path_no_empty(path, is_folder)
    is_folder = is_folder or 0

    local _type = if is_folder then "Folder" else "File"
    assert(#path > 0, `{_type} path must not be empty.`, 0)
end

local function _check_error_output(response: string)
    if response == "FILENOTFOUND_ERROR" then
        error("File does not exists.", 0)
    elseif response == "PERMISSION_ERROR" then
        error("Permission error.", 0)
    end
end

local filesystem = {}

function filesystem.isfile(path: string)
    c_assert(typeof(path) == "string", 1, {"string"})
    _path_no_empty(path)

    local is_success, response = bridge_post("isfile", {path})
    _check_error_output(response)

    return response
end

function filesystem.readfile(path: string)
    c_assert(typeof(path) == "string", 1, {"string"})
    _path_no_empty(path)

    local is_success, response = bridge_post("readfile", {path})
    _check_error_output(response)

    return response
end

function filesystem.writefile(path: string, data: string)
    c_assert(typeof(path) == "string", 1, {"string"}); _path_no_empty(path)
    c_assert(typeof(data) == "string", 2, {"string"})
    
    bridge_post("writefile", {path, data})
    _check_error_output(response)
end

function filesystem.delfile(path: string)
    c_assert(typeof(path) == "string", 1, {"string"})
    _path_no_empty(path)

    bridge_post("delfile", {path})
    _check_error_output(response)
end

function filesystem.listfiles(path: string): {string}
    c_assert(typeof(path) == "string", 1, {"string"})
    _path_no_empty(path, true)

    local is_success, response = bridge_post("listfiles", {path})
    _check_error_output(response)

    return response
end

function filesystem.isfolder(path: string)
    c_assert(typeof(path) == "string", 1, {"string"})
    _path_no_empty(path, true)

    local is_success, response = bridge_post("isfolder", {path})
    return response
end

function filesystem.makefolder(path: string)
    c_assert(typeof(path) == "string", 1, {"string"})
    _path_no_empty(path, true)

    bridge_post("makefolder", {path})
end

function filesystem.delfolder(path: string)
    c_assert(typeof(path) == "string", 1, {"string"})
    _path_no_empty(path, true)

    bridge_post("delfolder", {path})
end

return filesystem