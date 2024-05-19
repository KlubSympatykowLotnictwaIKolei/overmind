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
        self.drone_paths = {}

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
                        if not self.fly_to(drone_id, data["lat"] + offset_vector[0], data["lon"] + offset_vector[1]):
                            # If the path intersects with another drone, fly to a random location
                            random_angle = random.randint(0, 360) / 360 * 2 * math.pi

                            # 15 meters in latitude and longitude
                            offset_vector = (math.cos(random_angle) * 15 / 111_139, math.sin(random_angle) * 15 / 111_139)

                            if not self.fly_to(drone_id, data["lat"] + offset_vector[0], data["lon"] + offset_vector[1]):
                                # give up for now, maybe try again sometime later
                                continue
            except Exception as e:
                print(f"Error when decoding redis message\n{e}")
    def fly_to(self, drone_id, lat, lon) -> bool:
        # check if the path doesn't already intersect with a path of a different drone
        for other_drone_id, other_path in self.drone_paths.items():
            if drone_id == other_drone_id:
                continue
            if intersect_lines(
                self.drone_positions[drone_id].lat,
                self.drone_positions[drone_id].lon,
                lat,
                lon,
                self.drone_positions[other_drone_id].lat,
                self.drone_positions[other_drone_id].lon,
                other_path[0],
                other_path[1]
            ):
                print(f"Path intersects with drone {other_drone_id}")
                return False
        print(f"Sending drone {drone_id} to {lat}, {lon}")
        self.drone_paths[drone_id] = (lat, lon)
        self.redis.publish(f'command:fly_to:{drone_id}', json.dumps({ lat: lat, lon: lon }))

def intersect_lines(x1, y1, x2, y2, x3, y3, x4, y4) -> bool:
    # Check if the two lines intersect
    # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    x1, y1, x2, y2, x3, y3, x4, y4 = map(float, (x1, y1, x2, y2, x3, y3, x4, y4))
    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominator == 0:
        return False
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator
    return 0 <= t <= 1 and 0 <= u <= 1