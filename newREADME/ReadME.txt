一.Linux指令区：
(1)文件处理
	1.创建/删除文件夹：
		mkdir/rmdir ***
	2.创建多级文件夹：
		mkdir -p ****/****/***
	3.创建/删除（空）文件：
		touch/rm ***.***
	4.复制文件或文件夹：
		cp ****
	5.压缩/解压缩：
		zip/unzip -r ***.zip ***/
	6.进入指定目录：
		cd /***/***
(2）系统资源管理
	1.查看网络IP：
		ifconfig
	2.实时监控系统资源：
		top/htop
	3.显示系统内核及硬件信息：
		uname -a
	4.管理员权限：
		sudo
二.导航命令区：
(1)建图和定点
	1.建图：
		roslaunch /home/mowen/newznzc_ws/src/gmapping.launch
	2.定点获取新坐标：
		rostopic echo /move_base_simple/goal
(2)小车控制
	1.打开底盘数据：
		roscore
	2.打开底盘通信：
		rosrun car_bringup newt.py
	3.打开键盘控制：
		python ~/mbot_teleop/scripts/mbot_teleop.py
(3)导航
	1.打开RVIZ地图:
		roslaunch nav_demo nav777.launch
	2.导航主程序：
		python /home/mowen/newznzc_ws/src/PAN.py
三.视觉命令区：
(1)YOLO环境
	1.创建YOLO环境：
		conda create --name **** python=*.*
	2.进入YOLO环境：
		conda activate ***
(2)模型训练
	1.训练模型：
		yolo train model=*** data=****.yaml epochs=*** name=****
(3)调用视觉识别
	1.打开python文件：
		python3 /***/***/
	2.通过ros节点打开：
		roslaunch ****
四.后台管理命令区：
(1)导航：
	python3 /home/mowen/DH_HT/main.py
(2)视觉:
	python3 /home/mowen/BR_HT/BRHT.py
五.参数目录：
newznzc_ws/src/nav_demo/param/costmap_common_params.yaml 小车模型参数
newznzc_ws/src/nav_demo/param/dwa  小车速度参数
newznzc_ws/src/nav_demo/param  地图参数
newznzc_ws/src/leishen/lslidar_driver/launch第四个 雷达参数