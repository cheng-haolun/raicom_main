import sys
import time
import cv2
import serial
from ultralytics import YOLO

#串口初始化
def serial_init():
    serial_s = serial.Serial(
        port='/dev/ttyUSB0',  # 串口设备文件，根据实际情况修改
        baudrate=115200,  # 波特率，根据电机控制器要求设置
        bytesize=serial.EIGHTBITS,  # 数据位
        parity=serial.PARITY_NONE,  # 校验位
        stopbits=serial.STOPBITS_ONE,  # 停止位
        timeout=1  # 超时时间
    )
    print('serial_init success')
    return serial_s

#读入置信度等参数
def data_config():
    config_0={}
    with open('mbzz_HT/data.txt', encoding='UTF-8') as data_file:
        for line in data_file:
            key,value = line.strip().split(':', 1)
            config_0[key] = value
    return config_0

#初始化变量
config = data_config()
confident = float(config['confidence'])#置信度
image_size = int(config['image_size'])#识别尺寸
model_path = config['model_path']#模型路径
x_improve = 10#X轴瞄准补偿
y_improve = 10#Y轴瞄准补偿
angle_init = 0X5A#初始化角度
x_servo = 0X01#水平方向舵机编号
y_servo = 0X02#垂直方向舵机编号
fire_servo = 0X03#射击舵机编号
x_angel_sign = angle_init#水平角度状态
y_angel_sign = angle_init#垂直角度状态
fire = 0X01#开火状态
close = 0X00#关闭状态
ser = serial_init()#初始化串口
position_name = sys.argv[1]#点位信息
STATION = 0#开火状态

def position_get():
    global angle_init
    if position_name == 'position*':
        angle_init=0X5A
    elif position_name == 'position*':
        angle_init=0X01
    elif position_name == 'position*':
        angle_init=0X02
    elif position_name == 'position*':
        angle_init=0X03

#舵机初始化
def servo_init():
    ser.write(bytearray([0xAA, 0xBB, x_servo, angle_init, 0x0D, 0x0A]))#初始化水平舵机
    ser.write(bytearray([0xAA, 0xBB, y_servo, angle_init, 0x0D, 0x0A]))#初始化垂直舵机
    ser.write(bytearray([0xAA, 0xBB, fire_servo, close, 0x0D, 0x0A]))#初始化射击舵机
    print("servo init success")

#舵机瞄准及射击模块
def servo_move_and_fire(result_point_x,result_point_y,target_x,target_y):
    #水平舵机
    global STATION
    global x_angel_sign
    global y_angel_sign
    if target_x > result_point_x-x_improve:
        x_angel_sign+=1
        print("LEFT")
        ser.write(bytearray([0xAA, 0xBB, x_servo,x_angel_sign, 0x0D, 0x0A]))
        time.sleep(0.1)
    elif target_x < result_point_x+x_improve:
        x_angel_sign-=1
        print("RIGHT")
        ser.write(bytearray([0xAA, 0xBB, x_servo, x_angel_sign, 0x0D, 0x0A]))
        time.sleep(0.1)
    else:
        #垂直舵机
        if target_y < result_point_y+y_improve:
            y_angel_sign+=1
            print("UP")
            ser.write(bytearray([0xAA, 0xBB, y_servo, y_angel_sign, 0x0D, 0x0A]))
            time.sleep(0.1)
        elif target_y > result_point_y-y_improve:
            y_angel_sign-=1
            print("DOWN")
            ser.write(bytearray([0xAA, 0xBB, y_servo, y_angel_sign, 0x0D, 0x0A]))
            time.sleep(0.1)
    #开火
    if  result_point_x-x_improve<= target_x <= result_point_x+x_improve and result_point_y-y_improve<= target_y <= result_point_y+y_improve:
        print("GOOOOOOOOOAL!!!")
        time.sleep(1)
        ser.write(bytearray([0xAA, 0xBB, fire_servo, fire, 0x0D, 0x0A]))
        time.sleep(1)
        ser.write(bytearray([0xAA, 0xBB, fire_servo, close, 0x0D, 0x0A]))
        STATION=1

#结果绘制及判定模块
def show_result(frame,results):
    global ser,x_improve,y_improve
    target_x,target_y=int(image_size/2),int(image_size/2)#准心坐标信息
    for result in results:
        boxs = result.boxes
        for box in boxs:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            result_x=int((x1+x2)/2)#识别结果中心点x坐标
            result_y=int((y1+y2)/2)#识别结果中心点y坐标
            servo_move_and_fire(result_x,result_y,target_x,target_y)#瞄准并开火
            cv2.rectangle(frame,(result_x, result_y),(result_x+1,result_y+1),(225,0,0),2)#绘制识别结果中心点
            cv2.rectangle(frame,(x1, y1), (x2, y2), (0, 255, 0), 2)#绘制识别框
    cv2.rectangle(frame, (target_x,target_y), (target_x+1, target_y+1), (0, 255, 0), 2)#绘制中心点
    return frame

#模型及摄像头初始化模块
def init():
    global model_path
    cap = cv2.VideoCapture(2)#初始化摄像头
    #摄像头报错处理
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    model = YOLO(model_path)
    return cap, model

def main():
    global STATION
    if not ser.is_open:
        ser.open()
        print("串口打开成功")#打开串口
    cap,model=init()#初始化
    position_get()#获取点位信息
    servo_init()#初始化舵机
    while True:
        camera,frame=cap.read()#读取摄像头图像
        frame = cv2.resize(frame, (image_size, image_size))
        results = model.predict(source=frame, conf=confident,
                                stream=True,verbose=False,
                                imgsz=image_size)#识别结果
        frame=show_result(frame,results)#绘制结果并判定
        cv2.imshow('1',frame)
        time.sleep(0.5)
        if STATION == 1:
            break
        #遇到‘q’时停止
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break

if __name__ == '__main__':
    main()