local stub_index = 0
local stub_modules = {}

local utils = {}

function utils.to_hex(value: string)
    return string.gsub(value, ".", function(character)
        return string.format("%02X", string.byte(character))
    end)
end

function utils.from_hex(value: string)
    return string.gsub(value, "..", function(character)
        return string.char(tonumber(character, 16))
    end)
end

function utils.fetch_stub()
    stub_index = (stub_index % #stub_modules) + 1 -- not math.random cus that sometimes executes the previous script
    local stub_module = stub_modules[stub_index]

    return stub_module
end

function utils.c_assert(condition: boolean, arg_order: number, types: {string})
	if not condition then
		local reason = `Argument #{arg_order} must be a`
		for i, v in next, types do
			if i == #types and #types > 1 then
				reason = `{reason} or '{v}'`
				break
            end; reason = `{reason} '{v}' `
		end

		error(reason, 0)
	end
end

for _, v in next, game:GetService("CoreGui"):GetDescendants() do
    if v.ClassName == "ModuleScript" and v ~= script then
        local clone = v:Clone(); clone:ClearAllChildren()
        table.insert(stub_modules, clone)
    end
end

return utils