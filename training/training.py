from ultralytics import YOLO

DATASET_PATH = "data.yaml"

model = YOLO("yolov8s.pt")

model.train(
    data=DATASET_PATH,
    epochs=50,
    imgsz=640,
    batch=16,
    optimizer="SGD",
    lr0=0.005,
    project="runs",
    name="fire_truck_detector"
)
