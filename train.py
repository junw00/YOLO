import os
from ultralytics import YOLO

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Load a model
model = YOLO("yolov8m.yaml")  # build a new model from scratch
model = YOLO("yolov8m.pt")  # load a pretrained model (recommended for training)

if __name__ == '__main__':
    # Use the model
    model.train(data="D:/\hackathon_traning/data.yaml", epochs=10, batch=16, patience=50, imgsz=640)  # train the model
    model.val()