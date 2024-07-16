# -*- coding: utf-8 -*-
"""
@Brief: This is a test run script
@Version: Test Run 2.0.0
@author: Wang Yunkai
"""
import numpy as np
import VISION.visionmodule
import UI.Components as component
import BASE.GlobalData as data
LOG = False
VISION_PORT = 41001

ACTION_IP = '127.0.0.1'
ACTION_PORT = 20011
ROBOT_ID = 1

def get_vision_data(obj):
    visions = VISION.visionmodule
    vision = visions.VisionModule(VISION_PORT)
    # debug = visions.DEBUG(20001)
    while True:
        
        packge = vision.get_info(ROBOT_ID)
        robots_blue = packge.robots_blue
        robots_yellow = packge.robots_yellow
        ball = packge.balls
        pos = [ball.x,-ball.y]
        obj.set_ball(pos,ball.vel_x,ball.vel_y,ball.valid)
        obj.ball_data_time.append(data.time.total_time)
        
        for robot_yellow in robots_yellow:
            id_yellow = robot_yellow.robot_id
            pos_yellow = [robot_yellow.x,-robot_yellow.y]
            dir_yellow = robot_yellow.orientation
            tag_yellow = "YELLOW_" + str(int(id_yellow))
            obj.set_car(tag_yellow,pos = pos_yellow,dir = dir_yellow,show = True)
        for robot_blue in robots_blue:
            id_blue = robot_blue.robot_id
            pos_blue = [robot_blue.x,-robot_blue.y]
            dir_blue = robot_blue.orientation
            tag_blue = "BLUE_" + str(int(id_blue))
            obj.set_car(tag_blue,pos = pos_blue,dir = dir_blue,show = True)

