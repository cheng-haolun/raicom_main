#更新日志：该版本基于BRV2.0改进，该版本真正实现了目标检测并保存图片，优化了模型以及算法。
import cv2
import os
from ultralytics import YOLO

#读取文件信息
def data_config():
    config={}
    with open('BR_HT/data.txt') as data_file:
        for line in data_file:
            key,value = line.strip().split(':', 1)
            config[key] = value
    return config

def data_init():
    config = data_config()
    # 定义区
    confident = config['confidence']# 置信度
    num=config['num']# 图片编号
    model_path = config['model_path']  # 模型路径
    save_images = config['save_images']  # 原图保存路径
    return float(confident),int(num),model_path,save_images

def main():
    confident,num,model_path,save_images=data_init()
    result_id=0
    #加载模型
    model = YOLO(f'{model_path}')
    # 图片保存路径的判断，有则跳过，无则创建
    if not os.path.exists(f'{save_images}'):
        os.makedirs(save_images)

    # 查询可用摄像头索引号
    for camera_id in range(6):
        cap = cv2.VideoCapture(camera_id)  # 开启默认摄像头
        # 摄像头开启失败提醒
        if not cap.isOpened():
            print(f"{camera_id}无法打开")
        else:
            print(f"{camera_id}\n")
            cap.release()  # 释放摄像头

    camera_id = int(input("输入调用的摄像头"))
    cap= cv2.VideoCapture(camera_id)  # 开启摄像头

    while True:
        ret, frame = cap.read()
        cv2.imshow("Camera", frame)
        results = model.predict(source=frame, conf=confident,
                  stream=False)  # 识别图片
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        box=results[0].boxes
        if box:
            print('检测到目标')
            result_id += 1
            if result_id == 20:
                results[-1].show()
                results[-1].save(f'{save_images}/{num}.jpg')
                break
            else:
                print('未检测到目标')

    cap.release()
if __name__ == '__main__':
    main()