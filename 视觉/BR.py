#更新日志：该版本基于BRV2.0改进，该版本真正实现了目标检测并保存图片，优化了模型以及算法。
import cv2
import os
import sys
from ultralytics import YOLO
from PIL import ImageFont, ImageDraw, Image

def data_init():
    # 定义区
    confident = 0.85 #置信度
    num=1 #图片编号
    model_path ="/home/mowen/ultralytics-main/BRV11_improve_last/weights/best.pt"  # 模型路径
    save_images = "./BR_look" # 原图保存路径
    return float(confident),int(num),model_path,save_images

def get_chinese_and_save(img,im_path,font_path,font_size,text,position,color):

    try:
        font = ImageFont.truetype(font_path, font_size, encoding="utf-8")
    except IOError:
        raise FileNotFoundError(f"未找到字体文件，请检查路径：{font_path}")
    draw = ImageDraw.Draw(img)
    draw.text(position, text, font=font, fill=color)
    img.save(im_path)

def main():
    global position_id
    confident,num,model_path,save_images=data_init()
    result_id=0
    position=sys.argv[1]
    if position == 'position*5':
        position_id='D'
    elif position == 'position*7':
        position_id='C'
    elif position == 'position*22':
        position_id='B'
    elif position == 'position*24':
        position_id='A'
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
        count_rz=0
        count_yj=0
        count_dr=0
        results = model.predict(source=frame, conf=confident,
                  stream=False)  # 识别图片
        box=results[0].boxes
        if box:
            print('检测到目标')
            result_id += 1
            if result_id <= 2:
                results[0].show()
                results[0].save(f'{save_images}/{position}/{num}.jpg')
                for cls in results[0].boxes.cls:
                    if cls == 0:
                        count_yj += 1
                    elif cls == 1:
                        count_rz += 1
                    elif cls == 2:
                        count_dr += 1
                    elif cls == 3:
                        count_dr += 1
                im_path = f'{save_images}/{position}/{num}.jpg'
                font_path="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
                font_size=20
                position_txt=(0,0)
                color=(255,0,0)
                text=f'{position_id}区,人质：{count_rz}人,友军：{count_yj}人,敌人：{count_dr}人'
                img= Image.open(im_path)
                get_chinese_and_save(img,im_path,font_path,font_size,text,position_txt,color)
                num+=1
            else:
                break
        else:
            print('未检测到目标')
            
    print('goal')
    cap.release()

if __name__ == '__main__':
    main()