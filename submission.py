import json
import os

def json_to_txt():
    json_path = './runs/detect/val3/predictions.json'  # 评估结果文件路径
    data_root = './datasets/data/val'
    names = ['dent', 'pit', 'rust-spot', 'scratch', 'smudge']
    data_list = []
    for name in names:
        source_dir = os.path.join(data_root, f"{name}/images")
        files = sorted(os.listdir(source_dir))
        for file in files:
            basename, _ = os.path.splitext(file)
            data_list.append(basename)
    # 读取JSON文件
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    # 保存文件的路径
    output_dir = './runs/submisson_result'
    os.makedirs(output_dir, exist_ok=True)  # 如果目录不存在，创建它

    # 初始化一个字典来存储每个图片对应的检测框信息
    detections_by_image = {}

    # 遍历 JSON 数据中的每个检测信息
    for detection in data:
        image_id = detection['image_id']  # 获取图片ID
        label_id = detection['category_id']  # 获取类别
        label = names[label_id]
        bbox = detection['bbox']  # 获取检测框（中心点、宽度和高度）

        # bbox格式: [center_x, center_y, width, height]
        center_x, center_y, width, height = bbox

        # 转换为左上角 (x_min, y_min) 和右下角 (x_max, y_max) 坐标
        x_min = center_x - width / 2
        y_min = center_y - height / 2
        x_max = center_x + width / 2
        y_max = center_y + height / 2

        # 将结果存储为： [label, [x_min, y_min], [x_max, y_max]]
        detection_info = {
            "label": label,
            "bounding_box": [[x_min, y_min], [x_max, y_max]]
        }

        # 根据 image_id 将检测结果归类到一个字典中
        if image_id not in detections_by_image:
            detections_by_image[image_id] = []

        detections_by_image[image_id].append(detection_info)

    # 遍历每个图片的检测信息并写入对应的txt文件
    for image_id, detections in detections_by_image.items():
        txt_file_path = os.path.join(output_dir, f'{data_list[image_id - 2001]}.txt')

        with open(txt_file_path, 'w') as txt_file:
            for detection in detections:
                label = detection['label']
                (x_min, y_min), (x_max, y_max) = detection['bounding_box']
                # 写入文件，格式：类别 左上角坐标 右下角坐标
                txt_file.write(
                    f'{{"label":"{label}","bounding_box":[[{x_min},{y_min}],[{x_max},{y_max}]]}}\n')

        print(f'File saved: {txt_file_path}')

if __name__ == "__main__":
    json_to_txt()