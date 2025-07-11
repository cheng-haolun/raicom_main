import cv2
from ultralytics import YOLO

#读入置信度等参数
def data_config():
    config={}
    with open('mbzz_HT/data.txt', encoding='UTF-8') as data_file:
        for line in data_file:
            key,value = line.strip().split(':', 1)
            config[key] = value
    return config

#初始化变量
config = data_config()
confident = float(config['confidence'])#置信度
target_size = int(config['target_size'])#准心大小
image_size = int(config['image_size'])#识别尺寸
model_path = config['model_path']#模型路径

#结果绘制及判定模块
def show_result(frame,results):
    target_min,target_max=int((image_size/2)-(target_size/2)),int((image_size/2)+(target_size/2))#准心坐标信息
    #判断中心点是否在准心内
    for result in results:
        boxs = result.boxes
        for box in boxs:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            resultx=int((x1+x2)/2)
            resulty=int((y1+y2)/2)
            if target_min <= resultx <=target_max and target_min <= resulty <= target_max:
                print('YES')
            else:
                print(f'{resultx},{resulty}')
            cv2.rectangle(frame,(resultx, resulty),(resultx+1,resulty+1),(225,0,0),2)#绘制识别框
            cv2.rectangle(frame,(x1, y1), (x2, y2), (0, 255, 0), 2)#绘制识别结果中心点
    cv2.rectangle(frame, (target_min, target_min), (target_max, target_max), (225, 225, 0), 2)#绘制准心
    return frame

def show_zx(frame):
    cv2l = cv2.line
    cv2y = cv2.circle
    result = cv2l(frame,)

#初始化模块
def init():
    global model_path
    cap = cv2.VideoCapture(0)#初始化摄像头
    #摄像头报错处理
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    model = YOLO(model_path)
    return cap, model

def main():
    cap,model=init()#初始化
    while True:
        camera,zhen=cap.read()#读取摄像头图像
        zhen = cv2.resize(zhen, (image_size, image_size))
        results = model.predict(source=zhen, conf=confident,
                                stream=True,verbose=False,
                                imgsz=image_size)#识别结果
        frame=show_result(zhen,results)#绘制结果并判定
        cv2.imshow('zhen',frame)#输出结果
        #遇到‘q’时停止
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()