import os
import xml.etree.ElementTree as ET
import shutil
from tqdm import tqdm

# VOC 数据集路径
VOC_ROOT = "/root/motor-yolo/mydata/VOC_motor"
VOC_IMAGES = os.path.join(VOC_ROOT, "JPEGImages")
VOC_ANNOTATIONS = os.path.join(VOC_ROOT, "Annotations")
TRAIN_SET = os.path.join(VOC_ROOT, "ImageSets/Main/trainval.txt")  # 训练集
VAL_SET = os.path.join(VOC_ROOT, "ImageSets/Main/test.txt")  # 验证集

# 目标 COCO 格式路径
COCO_ROOT = "/root/motor-yolo/mydata/COCO_motor"
COCO_TRAIN_IMAGES = os.path.join(COCO_ROOT, "train/images")
COCO_TRAIN_LABELS = os.path.join(COCO_ROOT, "train/labels")
COCO_VAL_IMAGES = os.path.join(COCO_ROOT, "val/images")
COCO_VAL_LABELS = os.path.join(COCO_ROOT, "val/labels")

# 确保目录存在
os.makedirs(COCO_TRAIN_IMAGES, exist_ok=True)
os.makedirs(COCO_TRAIN_LABELS, exist_ok=True)
os.makedirs(COCO_VAL_IMAGES, exist_ok=True)
os.makedirs(COCO_VAL_LABELS, exist_ok=True)

# 读取 VOC 类别
def get_voc_classes():
    classes = set()
    for xml_file in os.listdir(VOC_ANNOTATIONS):
        tree = ET.parse(os.path.join(VOC_ANNOTATIONS, xml_file))
        root = tree.getroot()
        for obj in root.findall("object"):
            classes.add(obj.find("name").text)
    return sorted(list(classes))

# 解析 VOC XML 并转换为 YOLO 格式
def convert_voc_to_yolo(xml_path, class_map):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    size = root.find("size")
    img_w = int(size.find("width").text)
    img_h = int(size.find("height").text)

    yolo_data = []
    
    for obj in root.findall("object"):
        cls_name = obj.find("name").text
        cls_id = class_map[cls_name]

        bbox = obj.find("bndbox")
        xmin = float(bbox.find("xmin").text)
        ymin = float(bbox.find("ymin").text)
        xmax = float(bbox.find("xmax").text)
        ymax = float(bbox.find("ymax").text)

        # 计算中心点与宽高（归一化）
        x_center = (xmin + xmax) / 2.0 / img_w
        y_center = (ymin + ymax) / 2.0 / img_h
        width = (xmax - xmin) / img_w
        height = (ymax - ymin) / img_h

        yolo_data.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

    return yolo_data

# 处理数据集
def process_dataset(txt_file, image_dir, label_dir, dataset_name):
    with open(txt_file, "r") as f:
        image_list = f.read().strip().split("\n")

    voc_classes = get_voc_classes()
    class_map = {cls_name: i for i, cls_name in enumerate(voc_classes)}

    for image_name in tqdm(image_list, desc=f"Processing {dataset_name}"):
        xml_path = os.path.join(VOC_ANNOTATIONS, f"{image_name}.xml")
        img_path = os.path.join(VOC_IMAGES, f"{image_name}.jpg")

        if not os.path.exists(xml_path) or not os.path.exists(img_path):
            print(f"⚠️ 跳过 {image_name}: 文件缺失")
            continue

        # 转换 YOLO 标签
        yolo_labels = convert_voc_to_yolo(xml_path, class_map)
        if not yolo_labels:
            print(f"⚠️ 跳过 {image_name}: 无标注对象")
            continue

        # 复制图片
        new_img_path = os.path.join(image_dir, f"{image_name}.jpg")
        shutil.copy(img_path, new_img_path)

        # 保存 YOLO 标签
        label_path = os.path.join(label_dir, f"{image_name}.txt")
        with open(label_path, "w") as f:
            f.write("\n".join(yolo_labels))

# 转换训练集和验证集
process_dataset(TRAIN_SET, COCO_TRAIN_IMAGES, COCO_TRAIN_LABELS, "Train Set")
process_dataset(VAL_SET, COCO_VAL_IMAGES, COCO_VAL_LABELS, "Val Set")

print("✅ VOC 数据集成功转换为 COCO+YOLO 格式！")
