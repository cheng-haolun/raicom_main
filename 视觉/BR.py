#更新日志：该版本基于BRV2.0改进，该版本真正实现了目标检测并保存图片，优化了模型以及算法。
import cv2
import os
import sys
from ultralytics import YOLO

def data_init():
    # 定义区
    confident = 0.85 #置信度
    num=1 #图片编号
    model_path ="/home/mowen/ultralytics-main/BRV11_improve_last/weights/best.pt"  # 模型路径
    save_images = "./BR_look" # 原图保存路径
    return float(confident),int(num),model_path,save_images

def main():
    confident,num,model_path,save_images=data_init()
    result_id=0
    position=sys.argv[1]
    #加载模型
    model = YOLO(f'{model_path}')
    # 图片保存路径的判断，有则跳过，无则创建
    real_save_path = os.path.join(save_images,str(position))
    if not os.path.exists(real_save_path):
        os.makedirs(real_save_path)

    cap= cv2.VideoCapture(0)  # 开启摄像头

    while True:
        ret, frame = cap.read()
        cv2.imshow("Camera", frame)
        results = model.predict(source=frame, conf=confident,
                  stream=False)  # 识别图片
        box=results[0].boxes
        if box:
            print('检测到目标')
            result_id += 1
            if result_id <= 2:
                results[0].show()
                results[0].save(f'{save_images}/{position}/{num}.jpg')
                num+=1
            else:
                break
        else:
            print('未检测到目标')
            
    print('goal')
    cap.release()

if __name__ == '__main__':
    main()