import math

def format_number(number):
    return round(float(number), 2)

'''
自动配筋函数
As:: 所需钢筋面积
size:: 配置钢筋的截面尺寸
返回值:: [个数, 直径]
'''
def auto_steel(As, size=(400, 400), type='vertical'):
    # 存在以下直径的钢筋
    # diameters = [6, 8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32]
    # 更换钢筋优先级
    diameters = [20, 22, 25, 16, 18, 6, 8, 10, 12, 14,  28, 32]
    if type=='stirrup':
        diameters = [6, 8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32]
    spacings = [70, 75, 80, 85, 90, 95, 100, 110, 120, 125, 130,
               140, 150, 160, 170, 180, 190, 200, 220, 240, 250,
               260, 280, 300, 320]
    spacings.reverse()
    for desired_diameter in diameters:
        # 计算矩形截面的面积
        rect_width = rect_height = size[0]*1000
        # 计算所需直径的钢筋的面积
        steel_area = (3.14159 * desired_diameter ** 2) / 4
        if type == 'vertical':
            # 计算矩形截面上最多可以容纳多少根所需直径的钢筋，以满足间距要求 注意方形才可这样用
            max_num_bars = int(rect_width / (50 + desired_diameter))**2

            # 计算总共需要多少根所需直径的钢筋
            num_bars_needed = math.ceil(As / steel_area)

            # 设置限值不能全满布置
            if 0.5*max_num_bars > num_bars_needed:
                return [num_bars_needed, desired_diameter]
        elif type=='stirrup':
            for spacing in spacings:
                num_bars = 1000/spacing
                area = steel_area*num_bars
                if area > As:
                    return [spacing, desired_diameter]

    raise Exception('没有钢筋合适！！！')