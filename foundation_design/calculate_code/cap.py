import math
from tools import *
from appendix import *

# 承台类
class Cap:
    def __init__(self):
        # 埋深 单位为m
        self.depth = 0
        # 尺寸 单位为m
        self.size = ()
        # 自重
        self.weight = 0
        # 混凝土重度
        self.gama = 20
        # 柱子尺寸
        # 长宽 单位为m
        self.column_size = ()
        # 厚度 单位为m
        self.thickness = 0
        # 材料信息
        self.material_params = {}
        self.materials = {}
        # 钢筋面积 单位为mm2
        self.As = 0
        # 保护层厚度 单位为毫米
        self.protection_thickness = 0
        # 承台纵筋
        self.vertical_steel_result = []
        # 柱边到桩内边缘距离 以及角桩内边缘到承台外边缘
        self.a0x = 0
        self.a0y = 0
        self.c1 = 0
        self.c2 = 0
        # 冲垮比
        self.lambda_0x = 0
        self.lambda_0y = 0
        self.lambda_1x = 0
        self.lambda_1y = 0
        self.beta_0x = 0
        self.beta_0y = 0
        self.beta_1x = 0
        self.beta_1y = 0
        self.beta_hp = 0
        self.max_punching_below = 0
        self.max_punching_edge = 0


    '''
    注册柱子参数
    size 桩截面尺寸 元组
    '''
    def register_column(self, size):
        self.column_size = size

    '''
    注册承台参数
    depth 桩长 浮点数
    size 桩截面尺寸 元组
    auto 是否自动生成 布尔
    '''
    def register_cap(self, depth=1.7, size=(6, 6), thickness=1.5, auto=False):
        if auto:
            #TODO 自动生成承台参数，已经粗略完成
            '''
            depth 深度可以设置为通常深度，设置为1.5m
            size 根据所给尺寸限定个范围
            '''
            # 设置为柱子尺寸的6倍
            self.size = (math.ceil(self.column_size[0]*6), math.ceil(self.column_size[0]*6))
            # 设置为承台尺寸的1/4倍
            self.depth = self.size/4
            # 20cm以下
            self.thickness = self.depth - 0.2
        else:
            self.depth = depth
            self.size = size
            self.thickness = thickness

    '''
    注册材料信息
    material_params 材料信息 字典
    '''
    def register_material_params(self, materials):
        self.materials = materials
        self.material_params = {
            'Ec': elastic_modulus_concrete[materials['concrete']],
            'Es': elastic_modulus_steel[materials['steel']],
            'fc': concrete_compressive_design_strength[materials['concrete']],
            'fy': steel_tensile_design_strength[materials['steel']],
            'ft': concrete_tensile_design_strength[materials['concrete']]
        }

    '''
    计算承台自重
    '''
    def calc_self_weight(self):
        self.weight = self.size[0] * self.size[1] * self.depth * self.gama
        return self.weight

    '''
    承台配筋设计: 此处基本不做二次设计
    ::Nmax
    ::n
    ::protection_thickness 保护层厚度
    ::xi 距离中心的距离
    '''
    def cap_design(self, Nmax, n, protection_thickness=40, xi=2.275, x=[2.275, 2.275, 2.275, 2.275]):
        # TODO 非对称尺寸 目前只适合那样完全布满的 如 9 16
        # xi和x的设置不够智能
        self.xi = xi
        self.x = x
        self.protection_thickness = protection_thickness
        My = math.sqrt(n) * Nmax * self.xi
        h0 = self.thickness*1000 - protection_thickness
        self.As = My*1e6/(0.9*self.material_params['fy']*h0)
        self.vertical_steel_result = auto_steel(self.As, self.size)
        return self.vertical_steel_result

    '''
    承台冲切验算
    ::type 验算类型 below对应柱的向下冲切验算 edge对应角桩的冲切验算
    ::a0x 柱边到桩内边缘距离或角桩内边缘引冲切线与承台顶面交点的水平距离 m
    ::a0y 柱边到桩内边缘距离或角桩内边缘引 冲切线与承台顶面交点的水平距离 m
    ::c1 角桩内边缘至承台外边缘的距离(角桩验算时） m
    ::c2 角桩内边缘至承台外边缘的距离(角桩验算时） m
    '''
    def cap_punching_check(self, type='below', a0x=1.4, a0y=1.41, c1=1.15, c2=1.15, auto=False):
        ft = self.material_params['ft']
        h0 = self.thickness - self.protection_thickness/1000
        # TODO 自动识别柱边到桩内边缘距离 以及角桩内边缘到承台外边缘
        if auto:
            pass
        else:
            self.a0x = a0x
            self.a0y = a0y
        if type=='below':
            ac = self.column_size[0] * 1000
            bc = self.column_size[1] * 1000
            temp_c = 0.84
            temp_c1 = 2
            temp_c2 = 1
        else:
            # 此时ac和bc是角桩内边缘至承台外边缘的距离
            ac = c1 * 1000
            bc = c2 * 1000
            self.c1 = ac
            self.c2 = bc

            temp_c = 0.56
            temp_c1 = 1
            temp_c2 = 2
        # TODO self.a0y 和 self.a0x的修正
        if (self.a0x < h0 and 0.2*h0 > self.a0x) and (self.a0y < h0 and 0.2*h0 > self.a0y):
            pass
        else:
            pass
        # 计算冲跨比
        self.lambda_0x = self.a0x/h0
        self.lambda_0y = self.a0y/h0

        if 0.2 < self.lambda_0x < 1 and 0.2 < self.lambda_0y < 1:
            beta_0x = temp_c / (self.lambda_0x + 0.2)
            beta_0y = temp_c / (self.lambda_0y + 0.2)
            if type=='below':
                self.beta_0x = beta_0x
                self.beta_0y = beta_0y
            else:
                self.beta_1x = beta_0x
                self.beta_1y = beta_0y
        else:
            return 0
        # 截面高度影响系数
        self.beta_hp = get_beta_hp(h0*1000)
        # 单位kN
        max_punching = temp_c1 * (beta_0x * (bc + self.a0y * 1000 / temp_c2) + beta_0y * (
                    ac + self.a0x * 1000 / temp_c2)) * self.beta_hp * ft * h0
        if type=='below':
            self.max_punching_below = max_punching
        else:
            self.max_punching_edge = max_punching

        return max_punching









