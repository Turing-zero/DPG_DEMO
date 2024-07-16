import BASE.GlobalData as data
import dearpygui.dearpygui as dpg
import UI.Components as components
import math
import numpy as np
def get_close_mouse_car(obj):
    min_distance = 99999
    closest_tag = "canvs"
    mouse_pos = data.PARAM.mouse.pos
    for tag , car in  obj.show_car_data.items():
        pos = car["pos"]
        distance = calculate_distance(mouse_pos, pos)
        if distance < min_distance:
            min_distance = distance
            if min_distance <= data.PARAM.car.radius:
                closest_tag = tag
    data.PARAM.mouse.click_obj = closest_tag
    return closest_tag
def calculate_distance( pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
