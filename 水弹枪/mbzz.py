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

#初始化变量
confident = 0.5#置信度
image_size_x = 640#识别尺寸
image_size_y = 480
model_path = "/home/mowen/ultralytics-main/goal_modelNO.2/weights/best.pt"#模型路径
x_wide=0
y_wide=0
x_improve=0
y_improve=0
angel_improve_x=0
angel_improve_y=0
fz=0
angle_init = 0#初始化角度
x_servo = 0X01#水平方向舵机编号
y_servo = 0X02#垂直方向舵机编号
fire_servo = 0X03#射击舵机编号
fire = 0X01#开火状态
close = 0X00#关闭状态
ser = serial_init()#初始化串口
position_name = sys.argv[1]#点位信息
STATION = 0#开火状态

def position_get():
    global x_wide,y_wide,x_improve,y_improve,angel_improve_x,angel_improve_y,angle_init,x_angel_sign,fz
    if position_name == 'position*5':
        x_wide=10
        y_wide=30
        x_improve=1
        y_improve=1
        angel_improve_x=6
        angel_improve_y=-2
        angle_init=0X50
        fz=0
        x_angel_sign = angle_init#水平角度状态
    elif position_name == 'position*11':
        x_wide=15
        y_wide=40
        x_improve=1
        y_improve=-1
        angel_improve_x=2
        angel_improve_y=-1
        angle_init= 0X60
        fz=30
        x_angel_sign = angle_init#水平角度状态
    elif position_name == 'position*18':
        x_wide=15
        y_wide=30
        x_improve=0
        y_improve=0
        angel_improve_x=0
        angel_improve_y=1
        angle_init = 0XA0
        x_angel_sign = angle_init#水平角度状态
    elif position_name == 'position*24':
        x_wide=20
        y_wide=30
        x_improve=0
        y_improve=-1
        angel_improve_x=2
        angel_improve_y=-1
        angle_init=0X4A
        x_angel_sign = angle_init#水平角度状态

y_angel_sign = 0x5A#垂直角度状态
#舵机初始化
def servo_init():
    ser.write(bytearray([0xAA, 0xBB, x_servo, angle_init, 0x0D, 0x0A]))#初始化水平舵机
    ser.write(bytearray([0xAA, 0xBB, y_servo, 0x5A, 0x0D, 0x0A]))#初始化垂直舵机
    ser.write(bytearray([0xAA, 0xBB, fire_servo, close, 0x0D, 0x0A]))#初始化射击舵机
    print("servo init success")

#舵机瞄准及射击模块
def servo_move_and_fire(result_point_x,result_point_y,target_x,target_y):
    #水平舵机
    global STATION
    global x_angel_sign
    global y_angel_sign,x_wide,y_wide,x_improve,y_improve,fz,angel_improve_x,angel_improve_y
    x_control_min= target_x+x_improve - result_point_x+x_wide
    x_control_max= target_x+x_improve - result_point_x-x_wide
    y_control_min= target_y+y_improve - result_point_y+y_wide
    y_control_max= target_y+y_improve - result_point_y-y_wide
    if fz < x_control_min <25:
        x_angel_sign+=1
        print("litlle LEFT")
        ser.write(bytearray([0xAA, 0xBB, x_servo,x_angel_sign, 0x0D, 0x0A]))
        time.sleep(0.5)
    elif x_control_min > 25:
        x_angel_sign+=2
        print("large LEFT")
        ser.write(bytearray([0xAA, 0xBB, x_servo,x_angel_sign, 0x0D, 0x0A]))
        time.sleep(0.5)
    elif -25 < x_control_max< -fz:
        x_angel_sign-=1
        print("little RIGHT")
        ser.write(bytearray([0xAA, 0xBB, x_servo, x_angel_sign, 0x0D, 0x0A]))
        time.sleep(0.5)
    elif x_control_max < -25:
        x_angel_sign -= 2
        print("large RIGHT")
        ser.write(bytearray([0xAA, 0xBB, x_servo, x_angel_sign, 0x0D, 0x0A]))
        time.sleep(0.5)
    else:
        #垂直舵机
        if y_control_min>0:
            y_angel_sign+=1
            print("UP")
            ser.write(bytearray([0xAA, 0xBB, y_servo, y_angel_sign, 0x0D, 0x0A]))
            time.sleep(0.5)
        elif 0<y_control_min<10:
            y_angel_sign+=2
            print("UP")
            ser.write(bytearray([0xAA, 0xBB, y_servo, y_angel_sign, 0x0D, 0x0A]))
            time.sleep(0.5)
        elif -10 < y_control_max < 0:
            y_angel_sign-=1
            print("DOWN")
            ser.write(bytearray([0xAA, 0xBB, y_servo, y_angel_sign, 0x0D, 0x0A]))
            time.sleep(0.5)
        elif y_control_max < -10:
            y_angel_sign -= 2
            print("DOWN")
            ser.write(bytearray([0xAA, 0xBB, y_servo, y_angel_sign, 0x0D, 0x0A]))
            time.sleep(0.5)
    #开火
    if  result_point_x-x_wide-fz<= target_x+x_improve <= result_point_x+x_wide + fz and result_point_y-y_wide<= target_y+y_improve <= result_point_y+y_wide:
        print("GOOOOOOOOOAL!!!")
        ser.write(bytearray([0xAA, 0xBB, x_servo, x_angel_sign+angel_improve_x,0x0D, 0x0A]))
        time.sleep(0.5)
        ser.write(bytearray([0xAA, 0xBB, y_servo, y_angel_sign+angel_improve_y,0x0D, 0x0A]))
        time.sleep(0.5)
        ser.write(bytearray([0xAA, 0xBB, fire_servo, fire, 0x0D, 0x0A]))
        time.sleep(0.5)
        ser.write(bytearray([0xAA, 0xBB, fire_servo, close, 0x0D, 0x0A]))
        time.sleep(1)
        ser.write(bytearray([0xAA, 0xBB, x_servo,0x5A,0x0D,0x0A]))
        time.sleep(1)
        ser.write(bytearray([0xAA, 0xBB, y_servo,0x5A,0x0D,0x0A]))
        time.sleep(1)
        STATION=1

#结果绘制及判定模块
def show_result(frame,results):
    global ser,x_improve,y_improve
    target_x,target_y=int(image_size_x/2),int(image_size_y/2)#准心坐标信息
    for result in results:
        boxs = result.boxes
        for box in boxs:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            result_x=int((x1+x2)/2)#识别结果中心点x坐标
            result_y=int((y1+y2)/2)#识别结果中心点y坐标
            servo_move_and_fire(result_x,result_y,target_x,target_y)#瞄准并开火
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
        frame = cv2.resize(frame, (image_size_x, image_size_y))
        results = model.predict(source=frame, conf=confident,
                                stream=True,verbose=True,
                                imgsz=[image_size_x,image_size_y])#识别结果
        frame=show_result(frame,results)#绘制结果并判定
        if STATION == 1:
            break

if __name__ == '__main__':
    main()