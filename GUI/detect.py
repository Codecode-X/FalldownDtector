import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))  # 把 motor-yolo 目录添加到 Python 搜索路径
from yolov5.detect import detect_image

def detect_down(source, save_path, pt_path="best.pt"):
    """return True: 有！"""
    print(source)
    print(save_path)
    print(pt_path)
    
    # 检测
    detected_classes = detect_image(source, save_path, pt_path)
    # 判断有没有
    print("detected_classes: ", detected_classes)
    return "down" in detected_classes


if __name__ == "__main__":
    detect_down(None, None, None)