import numpy as np
import math
from collections import defaultdict
import re
import json
from scipy.interpolate import interp1d,interp2d
import matplotlib.pyplot as plt
import pandas as pd

#设置字体
plt.rcParams["font.sans-serif"]=["SimHei"]

# 杆件类
class Element:
    def __init__(self, p1, p2, E, A, I):
        # p1 p2为杆件的点
        self.p1 = p1
        self.p2 = p2
        # l为杆件长度
        self.l = np.linalg.norm(np.array((p1.x, p1.y)) -
                                np.array((p2.x, p2.y)))
        self.E = E
        self.A = A
        self.I = I
        # 线刚度
        self.i = self.E*self.I/self.l
        self.theta = math.atan2(p2.y - p1.y, p2.x - p1.x)
        self.node_link()

    # 设定点位间的关系
    def node_link(self):
        if self.theta != 0:
            if self.p1.y > self.p2.y:
                self.p1.link['down'] = self.p2
                self.p2.link['up'] = self.p1
            else:
                self.p1.link['up'] = self.p2
                self.p2.link['down'] = self.p1
        else:
            if self.p1.x > self.p2.x:
                self.p1.link['left'] = self.p2
                self.p2.link['right'] = self.p1
            else:
                self.p1.link['right'] = self.p2
                self.p2.link['left'] = self.p1

# 节点类
class Node:
    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.name = name
        self.link = {'up': None, 'down': None, 'left': None, 'right': None}
        # 用于记录各杆的内力弯矩
        self.moment = {'up': None, 'down': None, 'left': None, 'right': None}

# 定义结构的几何位置
class Structure:
    def __init__(self, nodes, elems, bc, load):
        # 传入节点字典
        self.nodes = nodes
        # 传入杆件字典
        self.elems = elems
        # 边界条件
        self.bc = bc
        self.fixed()
        # 荷载情况
        sorted_keys = sorted(load.keys(), reverse=True)

        cumulative_sum = 0
        transformed_dict = {}
        for key in sorted_keys:
            cumulative_sum += load[key]
            transformed_dict[key] = cumulative_sum
        self.load = transformed_dict
        # 各竖向轴的杆件
        self.axis_ele = defaultdict(list)
        self.extract_axis()

    # 提取各轴的杆件
    def extract_axis(self):
        for ele in self.elems:
            if self.elems[ele].theta != 0:
                self.axis_ele[self.elems[ele].p1.x].append(ele)

    def fixed(self):
        for f in self.bc:
            self.nodes[f].link['down'] = 'fixed'

# D值法的类
class D_value_method:
    def __init__(self, structure):
        self.structure = structure
        self.D_value_info = defaultdict(lambda: defaultdict(dict))
        self.n = len(structure.axis_ele[0])
        self.D_sum = defaultdict(lambda: 0)
        # 记录弯矩值以列表形式记录每根杆的弯矩，从上到下与从左到右的顺序
        self.M = defaultdict(list)

        # 加载json文件，反弯点表
        with open('./v0.json', 'r') as file:
            self.v0_t = json.load(file)
            for n in self.v0_t:
                for j in self.v0_t[n]:
                    x_known = list(map(lambda x:float(x), self.v0_t[n][j].keys()))
                    y_known = list(map(lambda x:float(x), self.v0_t[n][j].values()))
                    # 创建插值函数
                    interp_function = interp1d(x_known, y_known)
                    self.v0_t[n][j] = interp_function

        with open('./v1.json', 'r') as file:
            data = json.load(file)
            # 提取外部键作为一个维度
            x = np.array(list(map(float, data.keys())))

            # 假设所有外部键具有相同的内部键集合，提取这些内部键作为另一个维度
            inner_keys = list(map(float, list(data[next(iter(data))].keys())))
            y = np.array(sorted(inner_keys))

            # 创建值矩阵
            values = np.array([[data[str(x_val)].get(str(y_val), np.nan) for y_val in y] for x_val in x]).T
            # 创建 2D 插值函数
            self.v1_t = interp2d(x, y, values, kind='linear')

        with open('./v2.json', 'r') as file:
            data = json.load(file)
            # 提取外部键作为一个维度
            x = np.array(list(map(float, data.keys())))

            # 假设所有外部键具有相同的内部键集合，提取这些内部键作为另一个维度
            inner_keys = list(map(float, list(data[next(iter(data))].keys())))
            y = np.array(sorted(inner_keys))

            # 创建值矩阵
            values = np.array([[data[str(x_val)].get(str(y_val), np.nan) for y_val in y] for x_val in x]).T
            # 创建 2D 插值函数
            self.v2_t = interp2d(x, y, values, kind='linear')

        with open('./v3.json', 'r') as file:
            data = json.load(file)
            # 提取外部键作为一个维度
            x = np.array(list(map(float, data.keys())))
            # 假设所有外部键具有相同的内部键集合，提取这些内部键作为另一个维度
            inner_keys = list(map(float, list(data[next(iter(data))].keys())))
            y = np.array(sorted(inner_keys))
            # 创建值矩阵
            values = np.array([[data[str(x_val)].get(str(y_val), np.nan) for y_val in y] for x_val in x]).T
            # 创建 2D 插值函数
            self.v3_t = interp2d(x, y, values, kind='linear')

        # 计算alpha_c值
        self.alpha_c_cal()
        self.v_cal()
        self.D_cal()
        self.Vim_cal()
        self.M_cal()

    # 计算alphac
    def alpha_c_cal(self):
        for a in self.structure.axis_ele:
            for index, f in enumerate(self.structure.axis_ele[a]):
                # 这里的index+1是实际层数
                # 该层上部点对应的点位名称
                self.D_value_info[a][index + 1]['up_point'] = self.structure.nodes[f[-1]]
                self.D_value_info[a][index + 1]['h'] = self.structure.elems[f].l
                self.D_value_info[a][index + 1]['i'], \
                self.D_value_info[a][index + 1]['alpha_c'], \
                self.D_value_info[a][index + 1]['i_1'], \
                self.D_value_info[a][index + 1]['i_2'], \
                self.D_value_info[a][index + 1]['i_3'], \
                self.D_value_info[a][index + 1]['i_4'] = self.get_i_u(self.structure.elems[f].p1,
                                                                          self.structure.elems[f].p2)
                self.D_value_info[a][index + 1]['E'] = self.structure.elems[f].E
                self.D_value_info[a][index + 1]['I'] = self.structure.elems[f].I

    # 获取i值
    # 除底层外其余各层柱的线刚度应乘以 0.9 的修正系数 现浇楼板的中框架的线刚度要乘以2
    # 注意此函数只面向一般的情况，若要通用则应该进行更改
    def get_i_u(self, p1, p2):
        eles = self.structure.elems
        if p1.link['down'] != 'fixed':
            i_1 = eles[''.join(sorted(p2.name+p2.link['left'].name))].i*2 if p2.link['left']!=None else 0
            i_2 = eles[''.join(sorted(p2.name+p2.link['right'].name))].i*2 if p2.link['right']!=None else 0
            # 除底层外各层柱要乘以0.9
            i_c = eles[p1.name+p2.name].i*0.9
            i_3 = eles[''.join(sorted(p1.name+p1.link['left'].name))].i*2 if p1.link['left']!=None else 0
            i_4 = eles[''.join(sorted(p1.name+p1.link['right'].name))].i*2 if p1.link['right']!=None else 0
            i_u = (i_1+i_2+i_3+i_4)/2/i_c
            return i_u, i_u/(2+i_u), i_1, i_2, i_3, i_4
        else:
            i_1 = eles[''.join(sorted(p2.name+p2.link['left'].name))].i*2 if p2.link['left']!=None else 0
            i_2 = eles[''.join(sorted(p2.link['right'].name+p2.name))].i*2 if p2.link['right']!=None else 0
            i_c = eles[p1.name+p2.name].i
            i_3 = 0
            i_4 = 0
            i_u = (i_1 + i_2) / i_c
            return i_u, (0.5+i_u)/(2+i_u), i_1, i_2, i_3, i_4

    # 确定反弯点的位置
    def v_cal(self):
        for axial_i, axial in self.D_value_info.items():
            for f_i, f in axial.items():
                self.D_value_info[axial_i][f_i]['v0'] = \
                    float(self.v0_t[str(self.n)][f"{f_i}.0"](f['i']))

                alpha_1 = min((f['i_3']+f['i_4']), (f['i_1']+f['i_2']))\
                          /max((f['i_3']+f['i_4']), (f['i_1']+f['i_2']))
                self.D_value_info[axial_i][f_i]['v1'] = self.v1_t(alpha_1, f['i'])[0]
                if f_i == self.n:
                    self.D_value_info[axial_i][f_i]['v2'] = 0
                else:
                    alpha_2 = axial[f_i+1]['h']/f['h']
                    self.D_value_info[axial_i][f_i]['v2'] = self.v2_t(alpha_2, f['i'])[0]

                if f_i == 1:
                    self.D_value_info[axial_i][f_i]['v3'] = 0
                else:
                    alpha_3 = axial[f_i - 1]['h'] / f['h']
                    self.D_value_info[axial_i][f_i]['v3'] = self.v3_t(alpha_3, f['i'])[0]

                self.D_value_info[axial_i][f_i]['v'] = self.D_value_info[axial_i][f_i]['v0'] + \
                                                       self.D_value_info[axial_i][f_i]['v1'] + \
                                                       self.D_value_info[axial_i][f_i]['v2'] + \
                                                       self.D_value_info[axial_i][f_i]['v3']
                self.D_value_info[axial_i][f_i]['vh'] = self.D_value_info[axial_i][f_i]['v'] * \
                                                        self.D_value_info[axial_i][f_i]['h']

    def D_cal(self):
        for axial_i, axial in self.D_value_info.items():
            for f_i, f in axial.items():
                # 单位变为kn/m
                self.D_value_info[axial_i][f_i]['D1'] = 12*f['E']*f['I']/f['h']**3*10e-4
                self.D_value_info[axial_i][f_i]['D'] = self.D_value_info[axial_i][f_i]['D1']*f['alpha_c']
                # 计算Dsum
                self.D_sum[f_i] += self.D_value_info[axial_i][f_i]['D']

    # 计算反弯点处的弯矩
    def Vim_cal(self):
        for axial_i, axial in self.D_value_info.items():
            for f_i, f in axial.items():
                # 单位变为kn
                self.D_value_info[axial_i][f_i]['Vim'] = f['D']/self.D_sum[f_i]*self.structure.load[f_i]*10e-4

    # 计算弯矩
    def M_cal(self):
        for axial_i, axial in self.D_value_info.items():
            for f_i in sorted(axial.keys(), reverse=True):
                f = axial[f_i]
                self.D_value_info[axial_i][f_i]['M_c_up'] = (f['h'] - f['vh'])*f['Vim']
                self.D_value_info[axial_i][f_i]['M_c_down'] = f['vh'] * f['Vim']
                # 左右梁弯矩与相对线刚度有关
                if f_i == self.n:
                    # 如果是顶层
                    self.D_value_info[axial_i][f_i]['M_b_left'] = f['i_1']/(f['i_1']+f['i_2'])*\
                                                                  self.D_value_info[axial_i][f_i]['M_c_up']
                    self.D_value_info[axial_i][f_i]['M_b_right'] = f['i_2']/(f['i_1']+f['i_2'])*\
                                                                  self.D_value_info[axial_i][f_i]['M_c_up']
                else:
                    self.D_value_info[axial_i][f_i]['M_b_left'] = f['i_1'] / (f['i_1'] + f['i_2']) * \
                                                                  (self.D_value_info[axial_i][f_i]['M_c_up']+
                                                                   self.D_value_info[axial_i][f_i+1]['M_c_down'])
                    self.D_value_info[axial_i][f_i]['M_b_right'] = f['i_2'] / (f['i_1'] + f['i_2']) * \
                                                                  (self.D_value_info[axial_i][f_i]['M_c_up'] +
                                                                   self.D_value_info[axial_i][f_i + 1]['M_c_down'])
                # 配置节点的内力信息
                self.D_value_info[axial_i][f_i]['up_point'].moment['down'] \
                    = self.D_value_info[axial_i][f_i]['M_c_up']
                self.D_value_info[axial_i][f_i]['up_point'].link['down'].moment['up'] \
                    = self.D_value_info[axial_i][f_i]['M_c_down']
                self.D_value_info[axial_i][f_i]['up_point'].moment['left'] \
                    = self.D_value_info[axial_i][f_i]['M_b_left']
                self.D_value_info[axial_i][f_i]['up_point'].moment['right'] \
                    = self.D_value_info[axial_i][f_i]['M_b_right']

#为了更加方便对比几种数据所以这里改为了函数
def ins(fhand):
    print(fhand)
    nodes = dict()
    elems = dict()
    bc = list()
    load = dict()
    for line in fhand:
        line = re.split(",", line)
        if line[0] == 'node':
            nodes[line[1]] = Node(line[1], float(line[2]), float(line[3]))
        elif line[0] == 'element':
            elems[line[1]] = Element(nodes[line[1][0]], nodes[line[1][1]],
                                     float(line[2]), float(line[3]), float(line[4]))
        elif line[0] == 'BC':
            #有约束的会设为0
            #若无约束则为1
            bc.append(line[1])
        elif line[0] == 'force':
            load[int(line[1])] = float(line[2])

    frame = Structure(nodes, elems, bc, load)
    return frame

def get_nodes_moment(d_cal):
    # 绘制弯矩图
    nodes_moment = []
    for node in d_cal.structure.nodes:
        links = {}
        for l  in d_cal.structure.nodes[node].link:
            test = d_cal.structure.nodes[node].link[l]
            if test == 'fixed':
                links[l] = 'fixed'
            elif test == None:
                links[l] = None
            else:
                links[l] = d_cal.structure.nodes[node].link[l].name

        nodes_moment.append({'x': d_cal.structure.nodes[node].x, 'y': d_cal.structure.nodes[node].y,
            'name': d_cal.structure.nodes[node].name, 'link': links,
            'moment': d_cal.structure.nodes[node].moment})
    return nodes_moment


def get_table(d_cal):
    table = d_cal.D_value_info
    df = []
    # 遍历原始数据并提取所需的值
    for key, sub_dict in table.items():
        for sub_key, values in sub_dict.items():
            row = {
                '轴号id': key,
                '楼层': sub_key,
                '层高': values['h'],
                'i': values['i'],
                'alpha_c': values['alpha_c'],
                'v': values['v'],
                'D': values['D'],
                'Vim': values['Vim'],
                'M_c_up': values['M_c_up'],
                'M_c_down': values['M_c_down'],
                'M_b_left': values['M_b_left'],
                'M_b_right': values['M_b_right']
            }
            df.append(row)

    return df

