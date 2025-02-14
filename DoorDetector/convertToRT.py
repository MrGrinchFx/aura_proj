import torch
from ultralytics import YOLO



device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Load PyTorch model
model = YOLO("DoorDetector/Kemperv8.pt")

# Export the model to TensorRT
model.export(format="engine")