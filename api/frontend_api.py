import json
import websockets

from models.messages.MapMessage import MapMessage
from models.messages.StatusMessage import StatusMessage

class FrontendApi: 
    def __init__(self):
        self.websocket = websockets.connect('ws://128.0.0.1:8765')
        
    #{type: detections, detections: [drone_id: 5, object_class: 43, timestamp: 2343222, lat: 51.32332, lon: 22.432432]}
    async def send_map(self, map_message: MapMessage):
        detections = map_message.detections
        map_message = {"type": "detections", "detections": detections}
        await self.websocket.send(json.dumps(map_message))

    #{type: status, drones_online: 54}
    async def send_status(self, status_message: StatusMessage):
        status_message = {"type": "status", "drones_online": 54}
        await self.websocket.send(json.dumps(status_message))