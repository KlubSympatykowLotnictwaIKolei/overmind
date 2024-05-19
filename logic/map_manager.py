import random
from typing import List, Tuple
from models.messages.DetectionMessage import DetectionMessage


class MapManager:
    detections: dict #object_id to List[DetectionMessage]
    predictions: List[DetectionMessage]
    delta = 1 #miliseconds

    def push_detection(self, detection: DetectionMessage):
        (minKey, minDist) = (None, None)

        #get closest detection to the one we have here
        for (key,val) in self.detections.items():
            dist = self.calculate_distance(val[-1], detection)
            if(minDist is None or dist < minDist):
                (minKey, minDist) = (key, dist)

        if random.random() < 0.5: #todo: HOW THE FUCK DO I KNOW IF THIS IS THE TANK I ALREADY KNOW OR A NEW ONE? I KNOW HOW TO DO IT BUT IM TOO LAZY IDGAF
            self.detections[minKey].append(detection) #existing tank
        else:
            self.detections[len(self.detections)] = [detection] #new tank
            
    def get_map(self):
        #return union of detections and predictions
        self.calculate_predictions()

        list = []

        for (key, vals) in self.detections:
            for val in vals:
                list.append(val)
        for prediction in self.predictions:
            list.append(prediction)

        return list
    
    def calculate_predictions(self):
        #calculate predictions based on detections
        for (_,val) in self.detections.items():
            if(len(val) < 2):
                continue

            if val[-1].timestamp - self.timestamp_now() < self.delta and val[-2].timestamp - self.timestamp_now() < self.delta:
                prediction = self.get_prediction(val[-1], val[-2])
                self.predictions.append(prediction)

    def calculate_distance(self, detection1: DetectionMessage, detection2: DetectionMessage):
        return (detection1.lat - detection2.lat)**2 + (detection1.lon - detection2.lon)**2
    
    def timestamp_now(self,):
        pass

    def get_direction(self, detection1: DetectionMessage, detection2: DetectionMessage):
        pass

    def get_prediction(self, detection: DetectionMessage, last_known_position: DetectionMessage, speed: Tuple[float, float]):
        pass