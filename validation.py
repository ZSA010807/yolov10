from ultralytics import YOLOv10


model = YOLOv10('./runs/detect/train_yolov10b14/weights/best.pt')  #模型路径

model.val(data='ultralytics/cfg/datasets/defect.yaml', batch=4, device=0)