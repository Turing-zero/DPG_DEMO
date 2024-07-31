import dearpygui.dearpygui as dpg
import numpy as np

def apply_perspective_transform(x, y, matrix):
    """
    应用透视变换到给定的坐标 (x, y)
    :param x: 原始 x 坐标
    :param y: 原始 y 坐标
    :param matrix: 3x3 透视变换矩阵
    :return: 变换后的新坐标 (x', y')
    """
    # 计算新的坐标
    new_x = matrix[0]*x + matrix[1]*y + matrix[2]
    new_y = matrix[3]*x + matrix[4]*y + matrix[5]
    w = matrix[6]*x + matrix[7]*y + matrix[8]

    # 除以 w 得到真实坐标
    if w != 0:
        new_x /= w
        new_y /= w

    return new_x, new_y

def draw():
    """
    在 Dear PyGui 窗口中绘制原始矩形和透视变换后的矩形
    """
    with dpg.drawlist(width=400, height=400) as drawlist:
        # 原始坐标
        points = [(100, 100), (200, 100), (200, 200), (100, 200)]
        
        # 定义透视变换矩阵
        perspective_matrix = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0.001, 0.001, 1]
        ]).flatten().tolist()
        
        # 应用透视变换
        transformed_points = [apply_perspective_transform(x, y, perspective_matrix) for x, y in points]
        
        # 绘制原始矩形
        dpg.draw_polygon(points, color=(255, 0, 0, 255), fill=(255, 0, 0, 100))
        
        # 绘制透视变换后的矩形
        dpg.draw_polygon(transformed_points, color=(0, 255, 0, 255), fill=(0, 255, 0, 100))

def main():
    """
    主函数，创建 Dear PyGui 界面并启动
    """
    dpg.create_context()
    with dpg.window(label="Main Window"):
        draw()

    dpg.create_viewport(title='Custom Title', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()