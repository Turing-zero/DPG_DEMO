import dearpygui.dearpygui as dpg
import BASE.GlobalData as data
from BASE.GlobalData import PARAM as param
import numpy as np
import BASE.Utils as utils
import math
import UI.Components as componets
# 保存页面布局
def save_callback(sender, app_data, user_data):
    dpg.save_init_file("dpg_layout.ini")

# 左键拖动事件
def left_mouse_drag_callback(obj):
    click_name = data.PARAM.mouse.click_obj
    if data.PARAM.mouse.click_obj == "canvs":
        pass
    else:
        pass
        # show_car_data = obj.show_car_data
        # obj.set_car(tag = click_name,pos = data.PARAM.mouse.pos)
# 中键拖动事件
def middle_mouse_drag_callback():
    pass
def mouse_move_callback():
    # dpg.is_key_pressed
    if dpg.is_mouse_button_down(dpg.mvMouseButton_Middle):
        click_name = data.PARAM.mouse.click_obj
        center_x = param.canvs.width / 2
        center_y = param.canvs.height / 2
        translation_x ,translation_y,_ = param.canvs.translation
        move_x = param.mouse.pos[0] - param.mouse.pos_last[0] 
        move_y = param.mouse.pos[1] - param.mouse.pos_last[1]
        move_x,move_y = [move_x,move_y]

        if data.PARAM.mouse.click_obj == "canvs":
            # if param.mouse.pos == [mouse_x,mouse_y]:
            param.canvs.translation = [translation_x+move_x, translation_y+move_y, 0]
            param.canvs.translation_matrix = dpg.create_translation_matrix(param.canvs.translation)
        else:
            pass

def window_resize_callback():
    param.canvs.translation = [param.canvs.width /2,param.canvs.height /2,0]
    param.canvs.translation_matrix = dpg.create_translation_matrix(param.canvs.translation)

def mouse_click_callback(obj):
    param.mouse.click_pos = param.mouse.pos
    utils.get_close_mouse_car(obj)

def add_plot_time_shape():
    dpg.add_plot(label="Time Shape", parent="viewport_group")
def mouse_drag_callback():
    pass

def set_field_size(sender, app_data, user_data):
    w = int(app_data[0:2]) * 1000
    h = int(app_data[-1]) * 1000
    param.field.width = w
    param.field.height = h
    param.field.size = [w,h]
    print(param.field.size)

def mouse_wheel_handler(sender, app_data):
    mouse_x,mouse_y = dpg.get_mouse_pos()
    if (mouse_x < param.canvs.width and mouse_y < param.canvs.height):
        # app_data 包含滚轮滚动的值
        if data.PARAM.mouse.scale >= 0.3:
            step = 0.05
        else:
            step = 0.02
        if app_data > 0:
            data.PARAM.mouse.scale += step
        else:
            data.PARAM.mouse.scale -= step
        data.PARAM.mouse.scale = max(0.08, data.PARAM.mouse.scale)
        data.PARAM.mouse.scale = min(1.2, data.PARAM.mouse.scale)
        print(data.PARAM.mouse.scale)
        param.canvs.scales = [param.mouse.scale, param.mouse.scale, 1]
        param.canvs.scale_matrix = dpg.create_scale_matrix(param.canvs.scales)

def window_resize_handler():
    pass
    # # 平移
    # translation_vector = [param.canvs.width / 2,param.canvs.height / 2,1]
    # translation_matrix = dpg.create_translation_matrix(translation_vector)
    # dpg.apply_transform("canvs", translation_matrix)