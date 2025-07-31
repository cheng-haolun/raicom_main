# coding=utf-8
import serial
import time

def main():
    # 配置串口
    ser = serial.Serial(
        port='/dev/gun',  # 串口设备文件，根据实际情况修改
        baudrate=115200,  # 波特率，根据电机控制器要求设置
        bytesize=serial.EIGHTBITS,  # 数据位
        parity=serial.PARITY_NONE,  # 校验位
        stopbits=serial.STOPBITS_ONE,  # 停止位
        timeout=1  # 超时时间
    )

    # 定义要发送的信号序列
    signals = [
        bytearray([0xAA, 0xBB, 0x01, 0x3C, 0x0D, 0x0A]),
        bytearray([0xAA, 0xBB, 0x01, 0x78, 0x0D, 0x0A]),
        bytearray([0xAA, 0xBB, 0x01, 0x5A, 0x0D, 0x0A])
    ]

    try:
        # 打开串口
        if not ser.is_open:
            ser.open()
            print("Serial port opened successfully.")

        for i, signal in enumerate(signals, 1):
            # 发送信号
            ser.write(signal)
            print(f"Signal {i} sent:", ' '.join(f'0x{byte:02X}' for byte in signal))

            # 等待并读取响应
            time.sleep(0.1)  # 给设备响应时间
            response = ser.read(ser.in_waiting)  # 读取所有可用数据
            
            if response:
                print("Response received:", ' '.join(f'0x{byte:02X}' for byte in response))
            else:
                print("No response received.")

            # 如果不是最后一个信号，等待2秒
            if i < len(signals):
                print("Waiting 2 seconds before next signal...")
                time.sleep(2)

    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # 确保串口关闭
        if ser.is_open:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    main()