#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_srvs.srv  import    *
from actionlib import SimpleActionClient
from re import sub
import subprocess

client=None
goal_potions_BR=[0]#['position*5','position*7','position*24','position*26']
goal_potions_DB=[0]#['position*5','position*9','position*18','position*24']

def init():
    global client
    client = SimpleActionClient('move_base', MoveBaseAction)
    rospy.loginfo("等待move_base动作服务器...")
    client.wait_for_server()
    rospy.loginfo("已连接到move_base动作服务器")

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