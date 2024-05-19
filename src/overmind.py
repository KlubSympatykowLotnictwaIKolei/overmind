import asyncio
import json
from redis import Redis

from src.position import Position
import random
import math

class Overmind:
    def __init__(self):
        self.redis = Redis()
        self.pubsub = self.redis.pubsub()
        self.pubsub.psubscribe('position:*')
        self.pubsub.psubscribe('detection:*')
        self.drone_positions = {}
        self.detected_objects = []

    async def think(self):
        for message in self.pubsub.listen():
            # Sleep to allow other tasks to run (if necessary)
            await asyncio.sleep(0)
            print(message)
            try:
                if message['type'] == 'pmessage':
                    data = json.loads(message['data'])
                    [message, drone_id] = str(message["channel"]).split(":")
                    print(message)
                    if str(message) == "b'position":
                        self.drone_positions[drone_id] = Position(data["lat"], data["lon"], data["alt"], data["attitude"])
                    if message == "b'detection":
                        self.detected_objects.append(data)
                        random_angle = random.randint(0, 360) / 360 * 2 * math.pi

                        # 15 meters in latitude and longitude
                        offset_vector = (math.cos(random_angle) * 15 / 111_139, math.sin(random_angle) * 15 / 111_139)

                        # Follow the detected object
                        self.fly_to(drone_id, data["lat"] + offset_vector[0], data["lon"] + offset_vector[1])
            except Exception as e:
                print(f"Error when decoding redis message\n{e}")
    def fly_to(self, drone_id, lat, lon):
        self.redis.publish(f'command:fly_to:{drone_id}', json.dumps({ lat: lat, lon: lon }))
