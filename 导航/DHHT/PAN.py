#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_srvs.srv  import    *
from dynamic_reconfigure.client import Client
from actionlib import SimpleActionClient
from re import sub
import subprocess

client=None
dc_client=None
dc_client_dwa=None
goal_potions_BR=['position*5','position*7','position*22','position*24']
goal_potions_DB=['position*5','position*9','position*16','position*22']

def init():
    global client,dc_client,dc_client_dwa
    client = SimpleActionClient('move_base', MoveBaseAction)
    rospy.loginfo("等待move_base动作服务器...")
    client.wait_for_server()
    rospy.loginfo("已连接到move_base动作服务器")
    dc_client = Client('/move_base/local_costmap/inflation_layer')
    rospy.loginfo("已连接到 inflation_layer 动态参数")
    dc_client_dwa = Client('/move_base/DWAPlannerROS')

def fire(position_name):
        cmd = (
        'source /home/mowen/miniconda3/etc/profile.d/conda.sh && '
        'conda activate yolov8 && '
        'python3 /home/mowen/ultralytics-main/mbzz.py {0}'.format(position_name)
        )
        subprocess.Popen(['bash', '-l', '-c',cmd]).wait()

def stop_to_read(position_name):
        cmd = (
        'source /home/mowen/miniconda3/etc/profile.d/conda.sh && '
        'conda activate yolov8 && '
        'python3 /home/mowen/ultralytics-main/BR.py {0}'.format(position_name)
        )
        subprocess.Popen(['bash', '-l', '-c',cmd]).wait()

def data_init(path):
    try:
        goals={}
        key_list=[]
        with open(path) as file:
            for line in file:
                if '#' in line:
                    continue
                elif '!' in line:
                    break
                else:
                    key,value=line.strip().split(':',1)
                    points=value.split(',')
                    group_goals = []
                    group_goals.append([float(points[0]), float(points[1]), float(points[2]), float(points[3])])
                    goals[key]=group_goals
                    key_list.append(key)
        return goals,key_list
    except Exception , e:
        rospy.logerr("读取目标点文件失败: %s" % e)
        return {}, []

def navigate_to_point(x, y, z, w):
    global client
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.z = z
    goal.target_pose.pose.orientation.w = w
    client.send_goal(goal)
    rospy.loginfo("导航到目标: x=%.2f, y=%.2f, z=%.2f, w=%.2f" % (x, y, z, w))
    result = client.wait_for_result()
    if result:
        rospy.loginfo("导航完成！")
    else:
        rospy.logerr("导航失败！")
    return result

def main():
    global dc_client,client,dc_client_dwa
    data_path='/home/mowen/DHHT/datadh.txt'
    rospy.init_node('move_base_node')
    init()
    our_goals,key_list=data_init(data_path)
    for group_name in key_list:
        if group_name in goal_potions_BR and group_name in goal_potions_DB:
            stop_to_read(group_name)
            fire(group_name)
        else:
            if group_name in goal_potions_BR:
                stop_to_read(group_name)
            elif group_name in goal_potions_DB:
                fire(group_name)
        if group_name=="position*2":
            dc_client.update_configuration({'inflation_radius': 0.10})
            rospy.loginfo("局部膨胀半径已调整到 0.10 m")
            dc_client_dwa.update_configuration({'max_vel_x': 0.15,'max_vel_theta': 0.3})
        elif group_name == "position*3":
            dc_client.update_configuration({'inflation_radius': 0.03})
            rospy.loginfo("局部膨胀半径已调整到 0.03 m")
        elif group_name == "position*4":
            dc_client_dwa.update_configuration({'max_vel_x': 0.4,'max_vel_theta': 1.2,
                                                'occdist_scale':10,'stop_time_buffer':0.25})

        goals=our_goals[group_name]
        rospy.loginfo("处理组: %s" % sub(r'\*',' ',group_name))
        for goal in goals:
            rospy.loginfo("导航到新的目标位置...")
            result = navigate_to_point(*goal)
            if not result:
                rospy.logerr("导航失败，跳过下面的点")
                break

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation interrupted.")
    pass