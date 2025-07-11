#作者：程浩伦  学校：南京晓庄学院  创作时间：2025年6月2日 版本：V2.0  项目：睿抗兵人抽帧识别
#更新日志：该版本基于BRV1.1改进，该版本实现了文件读取获得数据，并拥有后台可视化程序进行修改,采用模块化编程，更加灵活,优化代码布局。
import cv2
import os
from ultralytics import YOLO

#读取文件信息
def data_config():
    config={}
    with open('BR_HT/data.chl') as data_file:
        for line in data_file:
            key,value = line.strip().split(':', 1)
            config[key] = value
    return config

def data_init():
    config = data_config()
    # 定义区
    confident = config['confidence']# 置信度
    num = config['num']  # 图片编号
    model_path = config['model_path']  # 模型路径
    save_images = './data_test/images'  # 原图保存路径
    return float(confident),int(num),model_path,save_images

def main():
    confident,num,model_path,save_images=data_init()
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
    cap = cv2.VideoCapture(camera_id)

    while True:
        save_path = os.path.join(save_images, f'image_{num}.jpg')
        camera, zhen = cap.read()
        if not camera:
            print("打开摄像头失败")  ##获取帧失败提醒
        else:
            cv2.imshow('Captured Image', zhen)  # 输出实时画面
            key = cv2.waitKey(1) & 0xFF  # 等待一个键盘输入
            if key == ord('s'):
                cv2.imwrite(save_path, zhen)  # 保存一帧
                num = num + 1
                print("保存成功")  # 保存成功提醒

            elif key == ord('q'):
                cap.release()  # 释放摄像头
                cv2.destroyAllWindows()  # 关闭摄像头实时画面
                break  # 跳出循环
    print("成功退出")  # 退出提醒
    print("正在识别中")
    model.predict(source='./data_test/images', conf=confident,
                  project='./data_test/', name='result',
                  save=True)  # 识别图片并保存
    print("完成")  # 完成提醒

main()