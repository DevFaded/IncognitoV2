import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from instance import Instance
from object_value import ObjectValue

ALLOWED_BRIDGE_TYPES = [str, int, bool]

class Bridge:
    def __init__(self):
        self.app = FastAPI()
        self.port = 9111

        self._callbacks_registry = {}
        self._requests_container = None

    def register_callback(self, callback):
        self._callbacks_registry[callback.__name__] = callback

    def register_library(self, module):
        if not "__library__" in module.__dict__:
            return None
        
        for callback in module.__library__:
            self.register_callback(callback)
    
    def parse_datas(self, data: dict) -> dict:
        if self._requests_container is None:
            return data

        new_data: list = []
        requests_data: Instance = self._requests_container[str(data["id"])]

        for value in data["values"]:
            value_type = type(value)

            if value_type == list and value[0] == "Instance" and requests_data is not None:
                instance: ObjectValue = ObjectValue(requests_data[value[1]])
                new_data.append(instance.value)
            elif value_type in ALLOWED_BRIDGE_TYPES:
                new_data.append(value)

        return new_data
    
    def handler(self):
        @self.app.api_route("/{callback_id}", methods = ["POST"])
        async def bridge_handler(request: Request):
            callbacks: dict = self._callbacks_registry
            callback_id: str = request.path_params["callback_id"]
            
            data = await request.json()
            if callback_id in callbacks:
                callback_response = {}

                callback_response = callbacks[callback_id](self.parse_datas(data))

                """
                try:
                    callback_response = callbacks[callback_id](self.parse_datas(data))
                except Exception as e:
                    callback_response = JSONResponse(
                        content = {"error": str(e)}, 
                        status_code = 500)
                    
                    return callback_response
                """
                
                return {"response": callback_response}
            
            return JSONResponse(
                content = {"error": "Callback not found"}, 
                status_code = 404)

    def run(self):
        self.handler()
        uvicorn.run(self.app, port = self.port, access_log = False)