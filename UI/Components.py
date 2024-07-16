import dearpygui.dearpygui as dpg
import UI.Language.Language as language
import UI.Theme as theme
import BASE.CallBack as callback
import math
import numpy as np
import BASE.GlobalData as data
import collections
from typing import Dict, List
class Object():

    def __init__(self):
        # 定义常量
        self.DEQUE_MAX_LEN = 800
        self.teams = ["BLUE", "YELLOW"]
        self.num_cars = 16
        # 初始化 car_data 字典
        self.show_car_data = {} 
        self.car_data = self.initialize_car_data()
        self.ball_data={
            "pos":[0,0],
            "vel_x":0,
            "vel_y":0,
            "vel":0,
            "valid":True
            }
        self.ball_data_vel = collections.deque(maxlen=self.DEQUE_MAX_LEN)
        self.ball_data_time = collections.deque(maxlen=self.DEQUE_MAX_LEN)
    def initialize_car_data(self):
        car_data = {}
        for team in self.teams:
            for i in range(self.num_cars):
                key = f"{team}_{i}"
                car_data[key] = {
                    "tag"  : key,
                    "pos"  : [0, 0],
                    "dir"  : 0,
                    "team" : team,
                    "show" : False,
                    "num"  : i
                }
        return car_data
    
    def plot_line(data_x,data_y,height,width):
        with dpg.plot(height=height, width=width):
            dpg.add_plot_legend()
            x_axis = dpg.add_plot_axis(dpg.mvXAxis,tag="xaxis",no_tick_labels=True)
            y_axis = dpg.add_plot_axis(dpg.mvYAxis,tag = "yaxis",no_tick_labels=True)
            ticks = [0, 1300, 2700, 4000, 5300, 6500, 8000]
            tick_labels = [[f"{x}", x, (255, 0, 0, 255)] if x == 6500 else [f"{x}", x, (255, 255, 0, 255)] for x in ticks]
            dpg.set_axis_ticks(x_axis, tick_labels)
            dpg.set_axis_limits(y_axis, 0, 8000)
            dpg.add_line_series(data_x, data_y, parent="yaxis",tag="line_series",label="Ball Vel")
    def set_ball(self,pos,vel_x,vel_y,valid):
        vel = math.sqrt(vel_x * vel_x + vel_y * vel_y)
        self.ball_data={
            "pos":pos,
            "vel_x":vel_x,
            "vel_y":vel_y,
            "vel":vel,
            "valid":True
            }
        self.ball_data_vel.append(vel)
    def set_car(self,tag,pos = None,dir = None,show = None):
        if pos:
            self.car_data[tag]["pos"] = pos
        if dir:
            self.car_data[tag]["dir"] = dir
        if show:
            self.car_data[tag]["show"] = show

    def show_car(self):
        for car in self.car_data.values():
            if car["show"]:
                pos = car["pos"]
                dir = car["dir"]
                tag = car["tag"]
                color = [0, 0, 255] if tag[0] == "B" else [255, 255, 0]
                self.draw_car(pos,data.PARAM.car.radius,dir,color,tag)

    def draw_ball(self):
        pos = self.ball_data["pos"]
        color = [255,165,0,255]
        dpg.draw_circle(center=pos,radius=47 * data.PARAM.mouse.scale,parent="canvs",color = color,thickness = 3,fill=color)
    def draw_car(self,pos, radius, dir,  color, tag):
        start_angle = 45 + dir * (180 / math.pi)
        end_angle = 315 + dir * (180 / math.pi)
        # 将角度转换为弧度
        start_radians = np.radians(start_angle)
        end_radians = np.radians(end_angle)
        # 计算每个分段的角度
        angles = np.linspace(start_radians, end_radians, 30 + 1)
        # 计算弧线上的点
        x = pos[0] + radius * np.cos(angles)
        y = pos[1] - radius * np.sin(angles)
        x2 = pos[0] + 200 * math.cos(-dir)
        y2 = pos[1] + 200 * math.sin(-dir)
        # 将点转换为列表格式
        points = np.column_stack((x, y)).tolist()
        dpg.draw_polygon(points, color=color, fill=color, parent="canvs",tag = tag,thickness=3)
        dpg.draw_text(text=self.car_data[tag]["num"],pos=np.array(pos) + (np.array([-147,-220])),parent = "canvs",size= 200 * data.PARAM.mouse.scale)
        # dpg.draw_arrow(p1=[x2,y2],p2 = pos, parent="canvs",size=15,thickness= 2.5,color=[0,255,255,80])
        
    def draw_field(self):
        color = [255,255,255,150]
        thickness = 4
        x,y = data.PARAM.field.size
        x = x / 2
        y = y / 2
        dpg.draw_rectangle(pmax=[-x,y],pmin=[x,-y],parent="canvs",color = color,thickness = thickness)
        dpg.draw_line(p1=[0,y],p2=[0,-y],parent="canvs",color = color,thickness = thickness)
        dpg.draw_line(p1=[x,0],p2=[-x,0],parent="canvs",color = color,thickness = thickness)
        dpg.draw_circle(center=[0,0],radius=500 * data.PARAM.mouse.scale,parent="canvs",color = color,thickness = thickness)
        if x == 4500:
            dpg.draw_rectangle(pmax=[-4500,1000],pmin=[-3500,-1000],parent="canvs",color = color,thickness = thickness)
            dpg.draw_rectangle(pmax=[3500,1000],pmin=[4500,-1000],parent="canvs",color = color,thickness = thickness)

    #清空画布
    def clean_canvs(self):
        dpg.delete_item("canvs",children_only=True)
        # self.car_data = self.initialize_car_data()
        
label = language.languages[theme.current_language]
def config_window():
    with dpg.window(tag="PARAM",label="PARAM"):
        with dpg.collapsing_header(label="Field"):
                dpg.add_text("Field Size：")
                # dpg.add_combo(items=["6000,4000", "9000,6000", "12000,9000"],tag="field_size_combo")
                dpg.add_listbox(items=["6 * 4","9 * 6","12 * 9"], default_value="9 * 6",tag="port_list",width=-1,callback=callback.set_field_size)

# 边菜单
def side_menu():
    # 右主内容 
    with dpg.child_window(tag="side_menu_right", width=-1,height=-1,pos=(10,15),show=True,drop_callback=callback.add_plot_time_shape,payload_type='Drag&Drop'):
        draw_window()
def plot_window():
    with dpg.window(tag="PLOT",label="PLOT"):
        Object.plot_line([],[],-1,-1)
# 画布
def draw_window():
    with dpg.drawlist(width=0, height=0,tag ="drawlist"):
        with dpg.draw_node(tag="config"):
            dpg.draw_text([10, 10],  color=[255, 255, 255, 255], size=40, tag="fps",text="Hello, world!")
        with dpg.draw_node(tag="canvs"):
            pass
