import json
from redis import Redis

from src.position import Position


class Overmind:
    def __init__(self):
        self.redis = Redis()
        self.pubsub = self.redis.pubsub()
        self.pubsub.psubscribe('position:*')
        self.pubsub.psubscribe('detection:*')
        self.drone_positions = {}
        self.detected_objects = {}

    def think(self):
        for message in self.pubsub.listen():
            print(message)
            try:
                if message['type'] == 'pmessage':
                    data = json.loads(message['data'])
                    [message, drone_id] = str(message["channel"]).split(":")
                    print(message)
                    if str(message) == "b'position":
                        self.drone_positions[drone_id] = Position(data["lat"], data["lon"], data["alt"], data["attitude"])
                    if message == "b'detection":
                        print(data)
            except Exception as e:
                print(f"Error when decoding redis message\n{e}")
    def fly_to(self, drone_id, lat, lon):
        self.redis.publish(f'command:fly_to:{drone_id}', json.dumps({ lat: lat, lon: lon }))
