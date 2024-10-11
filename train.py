from ultralytics import YOLOv10

# 数据集配置文件
data_yaml_path = 'ultralytics/cfg/datasets/defect.yaml'
# 训练模型配置文件
model_name = 'ultralytics/cfg/models/v10/yolov10b.yaml'

if __name__ == '__main__':
    # 加载预训练模型
    model = YOLOv10(model_name)
    # 训练生成的文件保存路径名
    savename = 'train_yolov10b'
    # 训练模型
    results = model.train(
                          data=data_yaml_path,
                          epochs=100,
                          name=savename)