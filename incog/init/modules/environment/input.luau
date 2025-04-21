-- Made by NiggerNinja December 15th, 2024 11:52 AM

local input_manager = Instance.new("VirtualInputManager")
local send_mouse_button_event = input_manager.SendMouseButtonEvent
local send_mouse_move_event = input_manager.SendMouseMoveEvent
local send_mouse_wheel_event = input_manager.SendMouseWheelEvent

local camera = workspace.CurrentCamera

local input = {}

function input.mouse1click(x, y)
    x, y = x or 0, y or 0

    send_mouse_button_event(input_manager, x, y, 0, true, game, false)
    task.wait()
    send_mouse_button_event(input_manager, x, y, 0, false, game, false) 
end

function input.mouse1press(x, y)
    x, y = x or 0, y or 0
    send_mouse_button_event(input_manager, x, y, 0, true, game, false)
end

function input.mouse1release(x, y)
    x, y = x or 0, y or 0
    send_mouse_button_event(input_manager, x, y, 0, false, game, false) 
end

function input.mouse2click(x, y)
    x, y = x or 0, y or 0
    send_mouse_button_event(input_manager, x, y, 1, true, game, false)
    task.wait()
    send_mouse_button_event(input_manager, x, y, 1, false, game, false) 
end

function input.mouse2press(x, y)
    x, y = x or 0, y or 0
    send_mouse_button_event(input_manager, x, y, 1, true, game, false)
end

function input.mouse2release(x, y)
    x, y = x or 0, y or 0
    send_mouse_button_event(input_manager, x, y, 1, false, game, false) 
end

function input.mousemoverel(x, y)
    viewport_size = camera.ViewportSize

    x, y = x or 0, y or 0
    x, y = viewportSize.X * x, viewportSize.Y * y
    send_mouse_move_event(input_manager, x, y, game)
end

function input.mousemoveabs(x, y)
    x, y = x or 0, y or 0
    send_mouse_move_event(input_manager, x, y, game)
end

function input.mousescroll(x, y, z)
    x, y, z = x or 0, y or 0, z or false
    send_mouse_wheel_event(input_manager, x, y, z, game)
end

return input