import json
import websockets

from models.messages.StatusMessage import StatusMessage

class FrontendApi: 
    async def __init__(self):
        self.websocket = await websockets.serve(self.handle_connection, 'localhost', 8765)
        # self.websocket = websockets.connect('ws://128.0.0.1:8765')

    async def handle_connection(self, websocket, path):
        self.websocket = websocket
        while True:
            message = await websocket.recv()


    #{type: detections, detections: [drone_id: 5, object_class: 43, timestamp: 2343222, lat: 51.32332, lon: 22.432432]}
    async def send_map(self, map_message):
        detections = map_message.detections
        map_message = {"type": "detections", "detections": detections}
        for socket in self.websocket.sockets:
            await socket.send(json.dumps(map_message))

    #{type: status, drones_online: 54}
    async def send_status(self, status_message: StatusMessage):
        status_message = {"type": "status", "drones_online": 54}
        for socket in self.websocket.sockets:
            await socket.send(json.dumps(status_message))