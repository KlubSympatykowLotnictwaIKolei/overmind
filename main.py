from api.frontend_api import FrontendApi
from logic.map_manager import MapManager
from src.overmind import Overmind
import asyncio

if __name__ == "__main__":
    overmind = Overmind()
    map_manager = MapManager()
    frontend_api = FrontendApi()
    
    last_detections_index = 0
    while True:
        asyncio.run(overmind.think()) #think
        detections = overmind.get_detection()[last_detections_index:] #act
        last_detections_index += len(detections) #skidable wooble

        map_manager.push_detection(detections) #push

        frontend_api.send_map(map_manager.get_map())
        frontend_api.send_status(len(overmind.get_drone_positions()))
        asyncio.sleep(1) #biden