import math
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'SimHei'

# 节点类
class Node:
    def __init__(self, name, x, y, nNode):
        #x坐标和y坐标
        self.x = x
        self.y = y
        self.name = name
        #节点自由度 实例化时会改变n值
        self.dof = [nNode * 3, nNode * 3 + 1, nNode * 3 + 2]

# 杆件类
class Element:
    def __init__(self, p1, p2, E, A, I):
        #p1 p2为杆件的点
        self.p1 = p1
        self.p2 = p2
        #l为杆件长度
        self.l = np.linalg.norm(np.array((p1.x, p1.y)) -
                                np.array((p2.x, p2.y)))
        self.E = E
        self.A = A
        self.I = I
        self.theta = math.atan2(p2.y - p1.y, p2.x - p1.x)
        self.klocal = self.klocal() #局部刚度矩阵
        self.T = self.trans()
        #整体刚度矩阵
        self.kglobal = np.linalg.multi_dot([self.T.transpose(),
                                            self.klocal, self.T])
        #杆件自由度
        self.dof = p1.dof + p2.dof #6个元素
        self.dglobal = np.zeros(6) #节点坐标系下的节点位移
        self.dlocal = np.zeros(6) #01坐标系下的节点位移
        self.flocal = np.zeros(6) #内力

    def klocal(self):
        E = self.E
        A = self.A
        l = self.l
        I = self.I
        matrix = np.matrix([[E * A / l, 0, 0, -E * A / l, 0, 0],
                            [0, 12 * E * I / l ** 3, 6 * E * I / l ** 2,
                             0, -12 * E * I / l ** 3, 6 * E * I / l ** 2],
                            [0, 6 * E * I / l ** 2, 4 * E * I / l, 0,
                             -6 * E * I / l ** 2, 2 * E * I / l],
                            [-E * A / l, 0, 0, E * A / l, 0, 0],
                            [0, -12 * E * I / l ** 3, -6 * E * I / l ** 2, 0,
                             12 * E * I / l ** 3, -6 * E * I / l ** 2],
                            [0, 6 * E * I / l ** 2, 2 * E * I / l, 0,
                             -6 * E * I / l ** 2, 4 * E * I / l]])
        return matrix

    def trans(self):
        T = np.matrix([[np.cos(self.theta), np.sin(self.theta), 0, 0, 0, 0],
                       [-np.sin(self.theta), np.cos(self.theta), 0, 0, 0, 0],
                       [0, 0, 1, 0, 0, 0],
                       [0, 0, 0, np.cos(self.theta), np.sin(self.theta), 0],
                       [0, 0, 0, -np.sin(self.theta), np.cos(self.theta), 0],
                       [0, 0, 0, 0, 0, 1]])
        return T


# 结构类
class Structure:
    def __init__(self, nodes, elems, bc, load):
        #传入节点字典
        self.nodes = nodes
        #传入杆件字典
        self.elems = elems
        #边界条件
        self.bc = np.array(bc)
        # 未被约束的自由度编号
        #挑选出无约束的自由度编号加入free中
        #0表示有约束 1表示无约束
        self.free = np.array([n for n, i in enumerate(self.bc) if i==1])

        #loadLite是精简后的力矩阵
        self.loadLite = np.array(load)[self.free]
        self.ndof = len(self.nodes) * 3
        self.K()
        self.calcForce()

    def K(self):
        #整个结构有多少个自由度就定义几阶矩阵
        self.kGlobal = np.zeros((self.ndof, self.ndof))
        for k, v in self.elems.items():
            for i in range(0, 6):
                for j in range(0, 6):
                    #此矩阵的行列号对应杆件的自由度编号
                    self.kGlobal[v.dof[i], v.dof[j]] += v.kglobal[i, j]
        self.kGlobal = self.kGlobal[self.free,:][:,self.free]

    def calcForce(self):
        self.disp = np.zeros(self.ndof)

        #d是简化后的总刚度矩阵求出来的位移 求出来的是一维向量
        d = np.linalg.multi_dot([np.linalg.inv(self.kGlobal), self.loadLite.T])

        #disp是总的刚度矩阵求出的位移 也就是这里需要把0给添加上
        np.add.at(self.disp, self.free, d)


        for k, v in self.elems.items():
            for i in range(0, 6):
                #为杆件的坐标系下的位移赋值
                v.dglobal[i] = self.disp[v.dof[i]]
            #转换坐标
            v.dlocal = np.linalg.multi_dot([v.T, v.dglobal])
            #算内力
            v.flocal = np.linalg.multi_dot([v.klocal, v.dlocal.T])


class Visual:

    def __init__(self, frame, title):
        self.frame = frame
        self.title = title #标题
        fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(1, 3,
                                                           sharex=True, figsize=(25, 15))
        self.force_map = {'moment': [2, 5, self.ax1],
                          'shear': [1, 4, self.ax2], 'axial': [0, 3, self.ax3]}
        fig.suptitle(title, fontsize=40)

    def draw(self, amp):
        #amp用于缩放
        for key in self.force_map:
            for k, v in self.frame.elems.items():
                m1 = Node("m1", v.p1.x + v.flocal[self.force_map[key][0], 0]
                          * np.cos(v.theta + np.pi / 2) / 1000 * amp,
                          v.p1.y + v.flocal[self.force_map[key][0], 0]
                          * np.sin(v.theta + np.pi / 2) / 1000 * amp, 0)
                m2 = Node("m2", v.p2.x - v.flocal[self.force_map[key][1], 0]
                          * np.cos(v.theta + np.pi / 2) / 1000 * amp,
                          v.p2.y - v.flocal[self.force_map[key][1], 0]
                          * np.sin(v.theta + np.pi / 2) / 1000 * amp, 0)

                self.force_map[key][2].plot(np.linspace(v.p1.x, v.p2.x, 10),
                                            np.linspace(v.p1.y, v.p2.y, 10), 'k-')
                self.force_map[key][2].plot(np.linspace(v.p1.x, m1.x, 10),
                                            np.linspace(v.p1.y, m1.y, 10), 'r-')
                self.force_map[key][2].plot(np.linspace(m1.x, m2.x, 10),
                                            np.linspace(m1.y, m2.y, 10), 'r-')
                self.force_map[key][2].plot(np.linspace(m2.x, v.p2.x, 10),
                                            np.linspace(m2.y, v.p2.y, 10), 'r-')
                self.force_map[key][2].text(m1.x-0.8, m1.y+0.4,
                                            '{0:.2g}'.format(
                                                abs(float(v.flocal[self.force_map[key][0], 0]) / 1e3)
                                            ), fontsize=12)
                self.force_map[key][2].text(m2.x+0.6, m2.y-0.4,
                                            '{0:.2g}'.format(
                                                abs(float(v.flocal[self.force_map[key][1], 0]) / 1e3)
                                            ), fontsize=12)
            self.force_map[key][2].set_title(key, fontsize=20)
        plt.show()


    def plotMoment(self, amp):
        for k, v in self.frame.elems.items():
            m1 = Node("m1", v.p1.x + v.flocal[2, 0] * np.cos(v.theta + np.pi / 2) / 1000 * amp,
                      v.p1.y + v.flocal[2, 0] * np.sin(v.theta + np.pi / 2) / 1000 * amp, 0)
            m2 = Node("m2", v.p2.x - v.flocal[5, 0] * np.cos(v.theta + np.pi / 2) / 1000 * amp,
                      v.p2.y - v.flocal[5, 0] * np.sin(v.theta + np.pi / 2) / 1000 * amp, 0)

            self.ax1.plot(np.linspace(v.p1.x, v.p2.x, 10), np.linspace(v.p1.y, v.p2.y, 10), 'k-')
            self.ax1.plot(np.linspace(v.p1.x, m1.x, 10), np.linspace(v.p1.y, m1.y, 10), 'r-')
            self.ax1.plot(np.linspace(m1.x, m2.x, 10), np.linspace(m1.y, m2.y, 10), 'r-')
            self.ax1.plot(np.linspace(m2.x, v.p2.x, 10), np.linspace(m2.y, v.p2.y, 10), 'r-')
        self.ax1.set_title("Moment", fontsize=20)
        plt.show()

    def plotShear(self, amp):
        #amp用于缩放
        for k, v in self.frame.elems.items():
            m1 = Node("m1", v.p1.x + v.flocal[1, 0] * np.cos(v.theta + np.pi / 2) / 1000 * amp,
                      v.p1.y + v.flocal[1, 0] * np.sin(v.theta + np.pi / 2) / 1000 * amp, 0)
            m2 = Node("m2", v.p2.x - v.flocal[4, 0] * np.cos(v.theta + np.pi / 2) / 1000 * amp,
                      v.p2.y - v.flocal[4, 0] * np.sin(v.theta + np.pi / 2) / 1000 * amp, 0)

            self.ax2.plot(np.linspace(v.p1.x, v.p2.x, 10), np.linspace(v.p1.y, v.p2.y, 10), 'k-')
            self.ax2.plot(np.linspace(v.p1.x, m1.x, 10), np.linspace(v.p1.y, m1.y, 10), 'r-')
            self.ax2.plot(np.linspace(m1.x, m2.x, 10), np.linspace(m1.y, m2.y, 10), 'r-')
            self.ax2.plot(np.linspace(m2.x, v.p2.x, 10), np.linspace(m2.y, v.p2.y, 10), 'r-')
        self.ax2.set_title("Shear", fontsize=20)
        plt.show()


    def plotAxial(self, amp):
        #amp用于缩放
        for k, v in self.frame.elems.items():
            m1 = Node("m1", v.p1.x + v.flocal[0, 0] * np.cos(v.theta + np.pi / 2) / 1000 * amp,
                      v.p1.y + v.flocal[0, 0] * np.sin(v.theta + np.pi / 2) / 1000 * amp, 0)
            m2 = Node("m2", v.p2.x - v.flocal[4, 0] * np.cos(v.theta + np.pi / 2) / 1000 * amp,
                      v.p2.y - v.flocal[3, 0] * np.sin(v.theta + np.pi / 2) / 1000 * amp, 0)

            self.ax3.plot(np.linspace(v.p1.x, v.p2.x, 10), np.linspace(v.p1.y, v.p2.y, 10), 'k-')
            self.ax3.plot(np.linspace(v.p1.x, m1.x, 10), np.linspace(v.p1.y, m1.y, 10), 'r-')
            self.ax3.plot(np.linspace(m1.x, m2.x, 10), np.linspace(m1.y, m2.y, 10), 'r-')
            self.ax3.plot(np.linspace(m2.x, v.p2.x, 10), np.linspace(m2.y, v.p2.y, 10), 'r-')
        self.ax3.set_title("Axial", fontsize=20)
        plt.show()


# Instantialization
#为了更加方便对比几种数据所以这里改为了函数
def ins(path='lilhard.csv'):
    fhand = open(path, encoding='utf-8')
    nodes = dict()
    elems = dict()
    bc = list()
    load = list()
    nNode = 0
    for line in fhand:
        line = re.split(",", line)
        if line[0] == 'node':
            nodes[line[1]] = Node(line[1], float(line[2]), float(line[3]), nNode)
            bc += [1, 1, 1]
            load += [0, 0, 0]
            nNode += 1
        elif line[0] == 'element':
            elems[line[1]] = Element(nodes[line[1][0]], nodes[line[1][1]],
                                     float(line[2]), float(line[3]), float(line[4]))
        elif line[0] == 'BC':
            #有约束的会设为0
            #若无约束则为1
            bc[int(line[1])] = 0
        elif line[0] == 'force':
            load[int(line[1])] = float(line[2])

    frame = Structure(nodes, elems, bc, load)
    return frame


frame = ins(path="kj.csv")
visual = Visual(frame, "矩阵位移法")
visual.draw(.05)

