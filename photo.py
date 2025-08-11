import cv2
import serial
import time

def camera_init():
    cap=cv2.VideoCapture(2)
    if not cap.isOpened():
        cap.open(2)
    return cap

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

def main():
    ser=serial_init()
    cap=camera_init()
    save_dir='/home/mowen/dbmodel'
    num=0
    x=0x5A
    y=0x5A
    while True:
        ret,frame=cap.read()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            ser.close()
            cap.release()
            break
        if cv2.waitKey(1) & 0xFF == ord('a'):
            x+=1
            time.sleep(0.1)
            ser.write(bytearray([0xAA, 0xBB, 0x01, x, 0x0D, 0x0A]))
        if cv2.waitKey(1) & 0xFF == ord('d'):
            x-=1
            time.sleep(0.1)
            ser.write(bytearray([0xAA, 0xBB, 0x01, x, 0x0D, 0x0A]))
        if cv2.waitKey(1) & 0xFF == ord('w'):
            y+=1
            time.sleep(0.1)
            ser.write(bytearray([0xAA, 0xBB, 0x02, y, 0x0D, 0x0A]))
        if cv2.waitKey(1) & 0xFF == ord('s'):
            y-=1
            time.sleep(0.1)
            ser.write(bytearray([0xAA, 0xBB, 0x02, y, 0x0D, 0x0A]))
        if cv2.waitKey(1) & 0xFF == ord('l'):
            cv2.imwrite(f'{save_dir}/{num}.jpg',frame)
            num+=1
cv2.destroyAllWindows()