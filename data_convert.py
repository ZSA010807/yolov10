import os
import shutil
import json

def copy_img_file(source_dir, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    # 获取源文件夹中的所有文件，按字母顺序排序
    files = sorted(os.listdir(source_dir))
    # 初始化计数器
    counter = len(os.listdir(target_dir)) + 1
    print(counter)
    # 遍历源文件夹中的文件
    for file_name in files:
        # 构造源文件的完整路径
        source_file = os.path.join(source_dir, file_name)
        # 检查是否为文件（而不是文件夹）
        if os.path.isfile(source_file):
            # 格式化新文件名为四位数，比如 0001.bmp
            new_filename = f"{counter:04d}.bmp"
            # 构造目标文件的完整路径
            target_file = os.path.join(target_dir, new_filename)
            # 复制文件并重命名
            shutil.copy(source_file, target_file)
            counter += 1
def convert_label_file(source_dir, target_dir, names, mode):
    files = sorted(os.listdir(source_dir))
    if mode == 'train':
        counter = len(os.listdir(target_dir)) + 1
    elif mode == 'val':
        counter = len(os.listdir(target_dir)) + 2001
    for file_name in files:
        # 构造源文件的完整路径
        source_file = os.path.join(source_dir, file_name)
        # 检查是否为文件（而不是文件夹）
        if os.path.isfile(source_file):
            with open(source_file, 'r') as json_file:
                data_json = json.load(json_file)
            data = data_json['shapes']
            # 打开txt文件准备写入
            txt_path = os.path.join(target_dir, f"{counter:04d}.txt")
            with open(txt_path, 'w') as txt_file:
                for item in data:
                    obj_class = item['label']  # 物体类别
                    obj_id = names.index(obj_class)
                    polygon = item['points']  # 包围框顶点，多边形形式

                    # 提取多边形所有顶点的x和y坐标
                    x_coords = [point[0] for point in polygon]
                    y_coords = [point[1] for point in polygon]

                    # 计算最小外接矩形框的顶点坐标
                    x_min = min(x_coords)
                    x_max = max(x_coords)
                    y_min = min(y_coords)
                    y_max = max(y_coords)

                    # 计算中心点 (x, y)，宽度 w 和高度 h
                    x_center = (x_min + x_max) / 2 / 1184  # 除以1184（img_size）目的是归一化坐标
                    y_center = (y_min + y_max) / 2 / 1184
                    width = (x_max - x_min) / 1184
                    height = (y_max - y_min) / 1184

                    # 写入txt文件，格式: class, x, y, w, h
                    txt_file.write(f"{obj_id} {x_center} {y_center} {width} {height}\n")
        counter = counter + 1
def rename():
    folder_path = '/opt/data/private/work/code/yolov10/datasets/data/images/val'
    files = sorted([f for f in os.listdir(folder_path) if f.endswith('.bmp')])

    # 起始编号
    start_num = 2001

    # 遍历文件并重命名
    for i, file_name in enumerate(files):
        # 生成新的文件名，例如 2001.txt, 2002.txt, ...
        new_name = f"{start_num + i:04d}.bmp"

        # 获取文件的完整路径
        old_file = os.path.join(folder_path, file_name)
        new_file = os.path.join(folder_path, new_name)

        # 重命名文件
        os.rename(old_file, new_file)

        print(f"Renamed {file_name} to {new_name}")

def main():
    data_root = './datasets/data'
    names = ['dent', 'pit', 'rust-spot', 'scratch', 'smudge']
    modes = ['train', 'val']
    copy_img = True
    convert_labels = True
    if copy_img:  #复制图片
        for mode in modes:
            target_dir = os.path.join(data_root, f"images/{mode}")
            for name in names:
                source_dir = os.path.join(data_root, f"{mode}/{name}/images")
                copy_img_file(source_dir, target_dir)
    if convert_labels:   #更改标签格式
        for mode in modes:
            target_dir = os.path.join(data_root, f"labels/{mode}")
            for name in names:
                source_dir = os.path.join(data_root, f"{mode}/{name}/labels")
                convert_label_file(source_dir, target_dir, names, mode)
if __name__ =="__main__":
    main()
