import cv2
from ultralytics import YOLO

WEIGHTS_PATH = "DoorDetector\Kemperv8.engine"

class DoorDetector:

  def __init__(self):
    self.weights = WEIGHTS_PATH
    self.model = YOLO(WEIGHTS_PATH, task="detect")

  def inference(self, frame):
    output = {
      "frame" : frame,
      "bounding_boxes" : [],
      "track_ids" : [],
      "annotation" : None
    }

    results = self.model.track(frame, conf=0.50, persist = True, verbose=False, device=0)

    if results[0].boxes.id is not None:
      output["track_ids"] = results[0].boxes.id.int().cpu().tolist()
      output["bounding_boxes"] = results[0].boxes.xyxy.cpu().tolist()

    output["annotation"] = results[0].plot()

    return output