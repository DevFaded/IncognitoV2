local BRIDGE_HOST = "http://127.0.0.1:9111/"
local ALLOWED_BRIDGE_TYPES = {"string", "boolean", "number"}

local http_service = game:GetService("HttpService")
local requests = Instance.new("Folder")

requests.Name = "BridgeRequests"; requests.Parent = script

local function _create_request_container(id)
    local request_container = requests:FindFirstChild(id)
    if not request_container then
        request_container = Instance.new("Folder")
        request_container.Name = id
        request_container.Parent = requests
    end

    return request_container
end

local function _create_instance_holder(index, instance, container)
    local instance_holder = container:FindFirstChild("I" .. index)
    if not instance_holder then
        instance_holder = Instance.new("ObjectValue")
        instance_holder.Name = "I" .. index
        instance_holder.Parent = container
    end; instance_holder.Value = instance

    return instance_holder
end

local bridge = {requests = requests}

function bridge.convert(id, data)
    local new_data = {}
    
    local instances = 0
    local request_container = _create_request_container(id)

    for i, v in next, data do
        local object_type = typeof(v)
        if object_type == "Instance" then
            _create_instance_holder(instances, v, request_container)
            
            table.insert(new_data, {object_type, instances}) -- instruction
            instances = instances + 1

        elseif table.find(ALLOWED_BRIDGE_TYPES, object_type) then
            table.insert(new_data, v)
        end
    end

    return new_data
end

function bridge.post(id, data)
    local response = Instance.new("BindableEvent")
    response.Event:Connect(function(...) return ... end)

    local new_data = http_service:JSONEncode(
        {["id"] = id, ["values"] = bridge.convert(id, data)})

    http_service:RequestInternal({
        Url = BRIDGE_HOST .. id,
        Method = "POST",
        Body = new_data
    }):Start(function(is_success, http_response)
        response:Fire(
            is_success,
            http_service:JSONDecode(
                http_response.Body).response
        )
    end)

    return response.Event:Wait()
end

function bridge.wait()
    while task.wait() do
        local response, success = bridge.post("client_ready", {})
        if success then
            print("Bridge connected!")
            break
        end

        warn("Failed to connect to bridge, retrying...")
    end
end

return bridge