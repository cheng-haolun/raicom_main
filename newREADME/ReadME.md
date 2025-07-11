# 目录
- [Linux指令区](#一Linux指令区)
  - [1.文件处理](#1文件处理)
    - 1.1创建/删除文件夹
    - 1.2创建多级文件夹
    - 1.3创建/删除（空）文件
    - 1.4复制文件或文件夹
    - 1.5压缩/解压缩
    - 1.6进入指定目录
  - [2.系统资源管理](#2系统资源管理)
    - 2.1查看网络IP
    - 2.2实时监控系统资源
    - 2.3显示系统内核及硬件信息
    - 2.4管理员权限
- [导航命令区](#二导航命令区)
  - [1.建图和定点](#1建图和定点)
    - 1.1显示系统内核及硬件信息
    - 1.2定点获取新坐标
  - [小车控制](#2小车控制)
    - 2.1打开底盘数据
    - 2.2打开底盘通信
    - 2.3打开键盘控制
  - [导航](#3导航)
    - 3.1打开Rviz地图
    - 3.2导航主程序
- [视觉命令区](#三视觉命令区)
  - [YOLO环境](#1YOLO环境)
    - 1.1创建YOLO环境
    - 1.2进入YOLO环境
  - [模型训练](#2模型训练)
    - 2.1训练模型
  - [调用视觉识别](#3调用视觉识别)
    - 3.1打开python文件
    - 3.2通过ros节点打开
- [后台管理命令区](#四后台管理命令区)
  - [导航](#1导航后台管理程序)
    - 1.1导航后台管理程序
  - [视觉](#2视觉后台管理程序)
    - 2.1视觉后台管理程序
- [参数目录](#五参数目录)
- [附录](#附录)
_____________________________
## 一.Linux指令区：

### (1)文件处理

***1.1 创建/删除文件夹：***
```bash
mkdir/rmdir
```
***1.2 创建多级文件夹：***
```bash
mkdir -p
```
***1.3 创建/删除（空）文件：***
```bash
touch/rm
```
***1.4 复制文件或文件夹：***
```bash
cp
```
***1.5 压缩/解压缩：***
```bash
zip/unzip -r ***.zip ***/
```
***1.6 进入指定目录：***
```bash
cd
```
- [返回目录](#目录)
### (2)系统资源管理
***2.1 查看网络IP：***
```bash
ifconfig
```
***2.2 实时监控系统资源：***
```bash
top/htop
```
***2.3 显示系统内核及硬件信息：***
```bash
uname -a
```
***2.4 管理员权限：***
```bash
sudo
```
- [返回目录](#目录)
_________________________________
## 二.导航命令区：

### (1)建图和定点：

***1.1 显示系统内核及硬件信息：***
```bash
roslaunch /home/mowen/newznzc_ws/src/gmapping.launch
```
***1.2 定点获取新坐标：***
```bash
rostopic echo /move_base_simple/goal
```
- [返回目录](#目录)
### (2)小车控制
***2.1 打开底盘数据：***
```bash
roscore
```
***2.2 打开底盘通信：***
```bash
rosrun car_bringup newt.py
```
***2.3 打开键盘控制：***
```bash
python ~/mbot_teleop/scripts/mbot_teleop.py
```
- [返回目录](#目录)
### (3)导航
***3.1 打开Rviz地图:***
```bash
roslaunch nav_demo nav777.launch
```
***3.2 导航主程序：***
```bash
python /home/mowen/newznzc_ws/src/PAN.py
```
- [返回目录](#目录)
________________________

## 三.视觉命令区：

### (1)YOLO环境

***1.1 创建YOLO环境：***
```bash
conda create --name ** python=*.*
```
***1.2 进入YOLO环境：***
```bash
conda activate
```
- [返回目录](#目录)
### (2)模型训练
***2.1 训练模型：***
```bash
yolo train model=*** data=****.yaml epochs=*** name=****
```
- [返回目录](#目录)
### (3)调用视觉识别
***3.1 打开python文件：***
```bash
python3 /***/***/***.py
```
***3.2 通过ros节点打开：***
```bash
roslaunch ****.launch
```
- [返回目录](#目录)
_______________________________
## 四.后台管理命令区：

### (1)导航后台管理程序：
```bash
python3 /home/mowen/DH_HT/main.py
```
### (2)视觉后台管理程序:
```bash
python3 /home/mowen/BR_HT/BRHT.py
```
- [返回目录](#目录)
_______________________________
## 五.参数目录：
### 小车模型参数:
***newznzc_ws/src/nav_demo/param/costmap_common_params.yaml***
### 小车速度参数
***newznzc_ws/src/nav_demo/param/dwa***
### 地图参数
***newznzc_ws/src/nav_demo/param***
### 雷达参数
***newznzc_ws/src/leishen/lslidar_driver/launch第四个***
- [返回目录](#目录)
___________________________
## 附录
### 视觉测试代码
```python
from ultralytics import YOLO

model=YOLO('yolov8.pt')

results=model.predict(source='bus.jpg',save=True)
```
### 查看摄像头编号
```python
import cv2

for camera_ID in range(5):
  
    cap=cv2.VideoCapture(camera_ID)

    if cap.isOpened():
      print(f"摄像头编号：{camera_ID}可用")
    else:
      print(f"摄像头编号：{camera_ID}不可用")
    cap.release()
```
- [返回目录](#目录)