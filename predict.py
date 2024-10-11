from ultralytics import YOLOv10

model = YOLOv10('./runs/detect/train_yolov10b14/weights/best.pt')
model.predict("./datasets/data/images/train/0100.bmp", imgsz=1184, save=True, device=0)