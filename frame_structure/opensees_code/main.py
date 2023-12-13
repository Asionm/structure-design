import math
import re
import numpy as np
import matplotlib.pyplot as plt
from openseespy.opensees import *

class Visual:
    def __init__(self, nodes_map, elems_map, element_forces, title):
        self.nodes_map = nodes_map
        self.elems_map = elems_map
        self.element_forces = element_forces
        self.title = title #标题
        fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(1, 3,
                                                           sharex=True, figsize=(25, 15))
        self.force_map = {'moment': [2, 5, self.ax1],
                          'shear': [1, 4, self.ax2], 'axial': [0, 3, self.ax3]}
        self.reverse = {'shear': 'axial', 'axial': 'shear'}
        fig.suptitle(title, fontsize=40)

    def draw(self, amp):
        #amp用于缩放
        for key in self.force_map:
            for k, v in self.elems_map.items():
                p1_x = self.nodes_map[k[0]][1]
                p1_y = self.nodes_map[k[0]][2]
                p2_x = self.nodes_map[k[1]][1]
                p2_y = self.nodes_map[k[1]][2]
                theta = math.atan2(self.nodes_map[k[1]][2] - self.nodes_map[k[0]][2],
                                   self.nodes_map[k[1]][1] - self.nodes_map[k[0]][1])
                if theta and key!='moment':
                    f_1 = element_forces[k][self.force_map[self.reverse[key]][0]]
                    f_2 = element_forces[k][self.force_map[self.reverse[key]][1]]
                else:
                    f_1 = element_forces[k][self.force_map[key][0]]
                    f_2 = element_forces[k][self.force_map[key][1]]




                self.force_map[key][2].plot(np.linspace(self.nodes_map[k[0]][1],
                                                        self.nodes_map[k[1]][1], 10),
                                            np.linspace(self.nodes_map[k[0]][2],
                                          self.nodes_map[k[1]][2], 10), 'k-')

                m1_x = p1_x + f_1 * np.cos(theta + np.pi / 2) / 1000 * amp
                m1_y = p1_y + f_1 * np.sin(theta + np.pi / 2) / 1000 * amp
                m2_x = p2_x - f_2 * np.cos(theta + np.pi / 2) / 1000 * amp
                m2_y = p2_y - f_2 * np.sin(theta + np.pi / 2) / 1000 * amp

                self.force_map[key][2].plot(np.linspace(p1_x, m1_x, 10),
                                            np.linspace(p1_y, m1_y, 10), 'r-')
                self.force_map[key][2].plot(np.linspace(m1_x, m2_x, 10),
                                            np.linspace(m1_y, m2_y, 10), 'r-')
                self.force_map[key][2].plot(np.linspace(m2_x, p2_x, 10),
                                            np.linspace(m2_y, p2_y, 10), 'r-')

                self.force_map[key][2].text(m1_x - 0.8, m1_y + 0.4,
                                            '{0:.2g}'.format(
                                                abs(float(f_1) / 1e3)
                                            ), fontsize=12)
                self.force_map[key][2].text(m2_x + 0.6, m2_y - 0.4,
                                            '{0:.2g}'.format(
                                                abs(float(f_2) / 1e3)
                                            ), fontsize=12)

            self.force_map[key][2].set_title(key, fontsize=20)
        plt.show()


# 加载数据
def load_data(path='kj.csv'):
    # 时间序列
    timeSeries("Linear", 1)
    # 荷载
    pattern("Plain", 1, 1)
    # 坐标转换
    geomTransf("Linear", 1)

    fhand = open(path, encoding='utf-8')
    nodes_map = dict()
    elems_map = dict()
    nNode = 1
    nElement = 1
    for line in fhand:
        line = re.split(",", line)
        if line[0] == 'node':
            nodes_map[line[1]] = [nNode, float(line[2]), float(line[3])]
            node(nNode,  float(line[2]), float(line[3]))
            nNode += 1
        elif line[0] == 'element':
            # 定义材料

            elems_map[line[1]] = [nElement, nodes_map[line[1][0]][0],
                                  nodes_map[line[1][1]][0]]
            # 定义杆件
            element("elasticBeamColumn", nElement, nodes_map[line[1][0]][0],
                    nodes_map[line[1][1]][0],
                    float(line[3]), float(line[2]), float(line[4]), 1)
            nElement += 1
        elif line[0] == 'BC':
            # 边界条件
            fix(nodes_map[line[1]][0], int(line[2]), int(line[3]), int(line[4]))

        elif line[0] == 'force':
            load(nodes_map[line[1]][0],int(line[2]), int(line[3]), int(line[4]))

        elif line[0] == 'load':
            if line[2] == 'beamUniform':
                eleLoad('-ele', elems_map[line[1]][0], '-type', '-beamUniform',
                        float(line[3]), float(line[4]))
            elif line[2] == 'beamGeneral':
                eleLoad('-ele', elems_map[line[1]][0], '-type', '-beamGeneral',
                        float(line[3]), float(line[4]), float(line[5]),
                            float(line[6]), float(line[7]))


    return elems_map, nodes_map


if __name__ == '__main__':
    # 初始化模型
    wipe()
    model('basic', '-ndm', 2, '-ndf', 3)  # 2D模型，每个节点有3个自由度（位移x, 位移y, 转角）
    elems_map, nodes_map = load_data(path='kj-opensees.csv')
    # 分析参数
    system("BandSPD")
    numberer("RCM")
    constraints("Plain")
    integrator("LoadControl", 1.0)
    algorithm("Linear")
    analysis("Static")

    # 执行分析
    analyze(1)

    element_forces = {}
    for elem_id, value in elems_map.items():
        forces = eleResponse(value[0], 'forces')
        element_forces[elem_id] = forces


    test = Visual(nodes_map, elems_map, element_forces, 'opensees')
    test.draw(.05)






