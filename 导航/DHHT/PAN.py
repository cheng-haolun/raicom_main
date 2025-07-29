#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import rospy
import tf
import actionlib
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal,MoveBaseActionResult,MoveBaseActionGoal
from std_srvs.srv  import    *
from actionlib import SimpleActionClient
from re import sub
import keyboard
import subprocess

client=None
goal_potions=['positon*','','','']

def init():
    global client
    client = SimpleActionClient('move_base', MoveBaseAction)
    rospy.loginfo("等待move_base动作服务器...")
    client.wait_for_server()
    rospy.loginfo("已连接到move_base动作服务器")

def stop_to_read():
    cmd = ("""
    cd ultralytics-main
    conda activate yolov8
    python3 BRv2.0.py
    """)
    subprocess.call(['bash','-c',cmd])

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
    except Exception as e:
        rospy.logerr("读取目标点文件失败: %s" % e)
        return {}, []

def navigate_to_point(x, y, z, w):
    global client
    try:
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
    except Exception,e:
        rospy.logerr("导航失败: %s" % e)
        return None
    except rospy.ROSException,e:
        rospy.logerr("ros错误: %s" % e)
        return None

def main():
    data_path='/home/mowen/DHHTV4.2/datadh.txt'
    rospy.init_node('move_base_node')
    init()
    our_goals,key_list=data_init(data_path)
    for group_name in key_list:
        if group_name in goal_potions:
            stop_to_read()
        if keyborad.is_pressed('q'):
            ros.loginfo("紧急中断程序！")
            ros.loginfo("中断的点为：%s" % sub(r'\*',' ',group_name))
            break
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