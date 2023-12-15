import math
from appendix import *
from tools import *
from cap import  Cap



# 桩基础类
class Foundation:
    def __init__(self):
        # 地层信息
        self.stratigraphic_info = []
        # 水文信息: 目前记录地下水埋深
        self.hydrologic_info = {}
        # 桩长
        self.length = 0
        # 桩截面尺寸，目前只基于方桩。
        self.size = (0, 0)
        # 承台
        self.cap = None
        # 截面面积
        self.Ap = 0
        # 周长
        self.u = 0
        # 创建qsk列表
        self.qsk_li = []
        # qpk桩端阻力
        self.qpk = 0
        # Quk 单桩承载力
        self.Quk = 0
        # 单桩承载力特征值
        self.Ra = 0
        # 桩数量
        self.n = 0
        # 受力参数
        self.force = {'Fk': 0, 'Mk': 0, 'Hk': 0}
        # 材料名称
        self.materials = {}
        # 材料信息
        self.material_params = {}
        # 保护层厚度
        self.protection_thickness = 40
        # 最小配筋率
        self.rho_g = 0.002
        # 桩身稳定系数
        self.varphi = 1.0
        # 预制桩桩身最小配筋率
        self.rho_min = 0.008
        # 桩身纵筋
        self.vertical_steel_result = []
        # 桩身箍筋
        self.stirrup_steel_result = []
        # 不记承台及其上土重Gk部分的净反力
        self.N = 0
        # 各桩平均竖向力（加上承台自重）
        self.Nk = 0
        # # 不记承台及其上土重Gk部分的净反力
        self.Nmax = 0
        self.Nkmax = 0
        # 桩身换算截面受拉边缘的截面模量，单位为mm3
        self.W0 = 0
        # #比例系数，此处先取6，单位为MN/m4 默认取6，缺乏详细的地层信息
        self.m = 6
        # 桩的水平变形系数单位为 1/m
        self.alpha = 0
        # 定桩顶（承台）的水平位移允许值 单位为mm 默认取10 规范P35
        self.x0a = 10
        self.alpha_h = 0
        # 设置寻找vx值 此处默认为固接，此处利用插值的方法取值
        self.vx = 0
        # 未考虑群桩效应的特征值
        self.Rha = 0
        # 桩中心距
        self.sa = 2.175
        # 两个方向桩数量
        self.n1 = self.n2 = 0
        self.eta_i = 0
        # eta_r的确定 同样通过拟合的方式
        self.eta_r = 0
        # 承台侧向土抗力效应系数
        self.eta_l = 0
        # 群桩效应综合系数
        self.eta_h = 0
        # 考虑群桩效应的特征值
        self.Rh = 0
        # 沉降计算
        self._varphi = 0
        self.pc0 = 0
        self.p0 = 0
        # 沉降地层信息
        self.H_T = []
        self.s_temp = 0
        self._Es = 0
        self.psai_p = 0
        # 最终沉降值
        self.s_final = 0
        # 抗剪验算
        self.ax1 = 0
        self.ax2 = 0
        self.beta_hs = 0
        self.shear_result1 = 0
        self.shear_result2 = 0
        # 桩身配筋
        self.temp_As = 0
        self.As = 0
        self.s_Asv = 0
        self.alpha_v = 0
        self.Asv = 0
        self.temp_Asv = 0

    def auto_calc(self, params):

        try:
            self.cap = Cap()
            self.cap.register_column(params['column_size'])
            self.cap.register_cap()
            self.cap.register_material_params(params['cap_materials'])
            self.register_material_params(params['fd_materials'])
            self.register_stratigraphic_info(params['stratigraphic_info'])
            self.register_hydrologic_info(params['underwater_depth'])
            self.register_force_params(params['force'])
            self.register_fd_params(length=params['pile_length'], size=params['pile_size'])
            self.calc_bearing_capacity()
            self.check_bearing_capacity()
            self.design_pile_body()
            self.design_cap()
            self.check_cap_punching()
            self.check_cap_punching(type='edge')
            self.check_shear_resist()
            self.check_shear_resist(section=2)
            self.calc_settlement()
        except Exception as e:
            print("Auto Calculate Failured!!!")
            print(e)

    '''
    初始化地层信息
    stratigraphic_info 完整的地层信息，类型为对象列表。
    '''
    def register_stratigraphic_info(self, stratigraphic_info):
        self.stratigraphic_info = stratigraphic_info

    '''
    添加地层信息:
     info 为要添加的地层信息，顺延添加。类型为字典。
    '''
    def add_stratigraphic_info(self, info):
        self.stratigraphic_info.append(info)

    '''
    去除地层信息
    index 需要去除的地层索引，默认为-1即默认去除最后一个地层。
    all 是否去除所有地层，默认为0即不去除所有，若为1则去除所有。
    '''
    def remove_stratigraphic_info(self, index=-1, all=0):
        if all:
            self.stratigraphic_info = []
        else:
            del self.stratigraphic_info[index]

    '''
    注册水文信息
    depth 地下水深度，浮点数。
    '''
    def register_hydrologic_info(self, depth):
        self.hydrologic_info['depth'] = depth

    '''
    注册基础参数
    length 桩长 浮点数
    size 桩截面尺寸 元组
    auto 是否自动生成 布尔
    '''
    def register_fd_params(self, length=0, size=(0, 0), auto=False):
        if auto:
            # TODO 自动生成基础参数（粗略完成）
            '''
            两个参数的确定思路：
            1. 首先是桩长度，桩长度的确定依赖于持力层。持力层的特征在于其坚硬长度，其坚硬长度或许可以通过粘聚力大大小来判定。
            同时桩长度应该有一定的值，不应该第一层就很坚硬就停留在第一层。桩长度根据规范需要深入持力层一定的深度，而此深度与桩截面
            存在关系，所以确定桩长度前需要先假设桩的截面尺寸。
            2. 其次是截面尺寸，截面尺寸可以先假设一个模糊值。其后面可能存在迭代更新的可能。因为初始设置的截面尺寸可能无法满足承载力的
            要求。
            '''
            # 总地层高度
            total_length = sum(list(map(lambda item: item['thickness'] , self.stratigraphic_info)))
            # 假设方桩尺寸 尺寸为米
            self.size = (0.2, 0.2)
            self.length = math.ceil(0.2*total_length)

            while 1:
                self.calc_bearing_capacity()
                capacity_check = self.check_bearing_capacity()
                vertical_check = capacity_check['vertical']
                horizontal_check = capacity_check['horizontal']
                # 粗略估计，此处严格遵守了9根的原则
                if self.n ** (1 / 2) * self.size[0] > 0.8 * self.cap.size[0] \
                        or self.n > 9 or vertical_check == 0 or horizontal_check == 0:
                    # 截面尺寸最大为1m, 大于1m则加大桩长
                    if self.size[0] < 0.7:
                        self.size = (self.size[0]+0.1, self.size[1]+0.1)
                    else:
                        if self.length < 0.8*sum(list(map(lambda item: item['thickness'] , self.stratigraphic_info))):
                            # 每次加1m
                            self.length += 1
                            # 根据规范
                            '''
                            应选择较硬土层作为桩端持力层。桩端全断面进入持力层的深度，对于黏性土、粉
                            土不宜小于 2d，砂土不宜小于 1.5d，碎石类土，不宜小于 1d。当存在软弱下卧层时，桩端
                            以下硬持力层厚度不宜小于 3d。
                            此处统一取3d
                            '''
                            cur_depth = 0
                            for item in self.stratigraphic_info:
                                cur_depth += item['thickness']
                                if self.length < cur_depth:
                                    insert_depth = item['thickness'] - (cur_depth - self.length)
                                    if insert_depth > 3*self.size[0]:
                                        break
                                    else:
                                        # 如果添加的深度仍然在此地层则添加否则添加6倍 仍然会出现特殊情况此处考虑并未周全
                                        if (cur_depth - self.length) > 3*self.size[0]:
                                            self.length += 3*self.size[0]
                                        else:
                                            self.length += 6*self.size[0]

                else:
                    break

        else:
            self.length = length
            self.size = size

    '''
    注册受力信息
    force 受力 字典
    '''
    def register_force_params(self, force):
        force['F'] = 1.35 * force['Fk']
        force['M'] = 1.35 * force['Mk']
        force['H'] = 1.35 * force['Hk']
        self.force = force

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
    注册承台
    cap 承台对象 Cap对象
    '''
    def bind_cap(self, cap):
        self.cap = cap

    '''
    单桩承载力计算
    sa:: 桩中心距
    '''
    def calc_bearing_capacity(self, sa=2.175):
        '''
        承载力计算所需要的参数：
        1.竖向：尺寸（面积、周长）、桩长、地层信息（输入）
        2.水平向（竖向基础上）：桩材料特性（手动输入）、最小配筋率（？固定）、保护层厚度（可以固定为40mm）、承台尺寸、承台厚度
        '''
        # 计算截面积
        self.Ap = self.size[0] * self.size[1]
        # 计算周长
        self.u = (self.size[0] + self.size[1]) * 2
        cur_depth = 0
        for item in self.stratigraphic_info:
            cur_depth += item['thickness']
            if self.length < cur_depth:
                self.qpk = item['qpk']
                self.qsk_li.append(item['qsk'] * (item['thickness'] - (cur_depth - self.length)))
                break
            else:
                # TODO 此处需要考虑承台高的影响
                self.qsk_li.append(item['qsk'] * item['thickness'])

        # 计算Quk
        self.Quk = self.qpk * self.Ap + sum(self.qsk_li) * self.u
        # 计算竖向承载力特征值
        self.Ra = self.Quk / 2
        # 确定竖向力即可确定桩数量
        self.confirm_num_layout()

        '''计算水平承载力特征值'''
        # 桩身换算截面受拉边缘的截面模量，单位为mm3
        self.W0 = self.size[0] * 1000 / 6 * ((self.size[0] * 1000) ** 2 +
                                        2 * (self.material_params['Es'] / self.material_params['Ec'] - 1)
                                        * self.rho_g * (self.size[0] - 2 * self.protection_thickness))
        # 桩身刚度
        self.EI = 0.85 * self.material_params['Ec'] * self.W0 * (self.size[0] * 1000 - 2 * self.protection_thickness) / 2
        # 单位转换 转为kNm2
        self.EI = self.EI * 1e-9
        if self.size[0] < 1:
            # 桩身计算长度
            b0 = 1.5 * self.size[0] + 0.5
        else:
            b0 = self.size[0] + 1

        # 桩的水平变形系数单位为 1/m
        self.alpha = (self.m * 10 ** (3) * b0 / self.EI) ** (1 / 5)

        if self.alpha * self.length > 4:
            self.alpha_h = 4
        else:
            self.alpha_h = self.alpha * self.length

        #设置寻找vx值的规则 规范表5.7.2  此处默认为固接，此处利用插值的方法取值
        self.vx = f_vx(self.alpha_h)
        # 未考虑群桩效应的特征值
        self.Rha = (0.75 * self.alpha ** (3) * self.EI * self.x0a * 1e-3) / self.vx

        # TODO 中心距如何确定 self.n1与self.n2的确定 self.n1 与 self.n2默认一样 粗略完成存在Bug
        self.sa = sa
        self.n1 = self.n2 = math.ceil(self.n ** (1 / 2)) if math.ceil(self.n ** (1 / 2)) > 0 else 0.0001
        self.eta_i = (sa / self.size[0]) ** (0.015 * self.n2 + 0.45) / (0.15 * self.n1 + 0.1 * self.n2 + 1.9)
        # eta_r的确定 同样通过拟合的方式
        self.eta_r = f_eta_r(self.alpha_h)
        # 承台侧向土抗力效应系数
        self.eta_l = (self.m * 10 ** 3 * self.x0a * 1e-3 * (self.cap.size[0] + 1) * self.cap.depth ** 2) \
                / (2 * self.n1 * self.n2 * self.Rha)
        # 群桩效应综合系数
        self.eta_h = self.eta_i * self.eta_r + self.eta_l
        # 考虑群桩效应的特征值
        self.Rh = self.eta_h * self.Rha


        '''
        计算单桩所承受的力
        '''
        self.Nk = (self.force['Fk'] + self.cap.calc_self_weight()) / self.n
        # 不记承台及其上土重Gk部分的净反力
        self.N = self.force['F'] / self.n
        # 最大值
        if self.force['Mk'] or self.force['Hk']:
            # TODO 手动设置
            xi = 2.275
            x = [2.275, 2.275, 2.275, 2.275]
            self.Nkmax = self.Nk + ((self.force['Mk'] + self.force['Hk'] * self.cap.depth) * xi) / sum(
                map(lambda item: item ** 2, x))
            # 不加承台自重
            self.Nmax = self.N + 1.35*((self.force['Mk'] + self.force['Hk'] * self.cap.depth) * xi) / sum(
                map(lambda item: item ** 2, x))

        return {'Ra': self.Ra, 'Rh': self.Rh}

    '''
    沉降计算
    仅使用实体深基础中的荷载扩散法进行计算
    '''
    def calc_settlement(self):
        a, b = self.cap.size
        # TODO 群桩外缘矩形面积的长短边长度，此处取距边缘1m
        a0 = a -1
        b0 = b -1
        l = self.length
        self._varphi = 0
        cur_depth = 0
        for item in self.stratigraphic_info:
            cur_depth += item['thickness']
            if self.length < cur_depth:
                self._varphi += (item['thickness'] - (cur_depth - self.length))/l*item['phi']
                break
            else:
                # TODO 此处需要考虑承台高的影响
                self._varphi += item['thickness']/l*item['phi']
        #TODO 承台底面高程处地基土的自重压力 此处默认第一层土直接覆盖承台
        self.pc0 = self.stratigraphic_info[0]['gama']*self.cap.depth

        self.p0 = (self.force['F']+self.cap.weight-self.pc0*a*b)/ \
             ((b0+2*l*math.tan(math.pi*self._varphi/180/4))*\
             (a0+2*l*math.tan(math.pi*self._varphi/180/4)))

        # 分层表 2m一层若小于2m则单独取 从桩底开始
        span = 2
        self.H_T = []
        s = 0
        A = 0
        A_Es = 0


        cur_depth = 0
        for item in self.stratigraphic_info:
            cur_depth += item['thickness']
            if self.length < cur_depth:
                # 如果是第一层
                if cur_depth - self.length < item['thickness']:
                    self.H_T.append({'z_m': 0, 'z_b': 0, '_a': 1.,
                                'Es': item['Es'], 's': 0, 'A': 0})
                    if cur_depth - self.length < span:
                        z = cur_depth - self.length
                        z_b = z/b
                        _a = f_a(z_b, a/b)[0]
                        si = self.p0/item['Es']*(z*_a-self.H_T[-1]['z_m']*self.H_T[-1]['_a'])
                        temp = {'z_m': z,
                                'z_b': z_b,
                                '_a': _a,
                                'Es': item['Es'],
                                's': si,
                                'A': item['Es']*si}
                        self.H_T.append(temp)
                    else:
                        h = cur_depth - self.length
                        while h > span:
                            z = self.H_T[-1]['z_m'] + span
                            z_b = z/b
                            _a = f_a(z_b, a/b)[0]
                            si = self.p0 / item['Es'] * (z * _a - self.H_T[-1]['z_m'] * self.H_T[-1]['_a'])
                            temp = {'z_m': z, 'z_b': z_b, '_a': _a,
                                    'Es': item['Es'], 's': si, 'A': item['Es']*si}
                            self.H_T.append(temp)
                            h -= span

                            if self.H_T[-1]['s'] < 0.025 * s:
                                break
                            else:
                                s += self.H_T[-1]['s']
                                A += self.H_T[-1]['A']
                                A_Es += self.H_T[-1]['A'] / self.H_T[-1]['Es']

                        if h:
                            z = self.H_T[-1]['z_m'] + h
                            z_b = z / b
                            _a = f_a(z_b, a/b)[0]
                            si = self.p0 / item['Es'] * (z * _a - self.H_T[-1]['z_m'] * self.H_T[-1]['_a'])
                            temp = {'z_m': z, 'z_b': z_b, '_a': _a,
                                    'Es': item['Es'], 's': si, 'A': item['Es'] * si}
                            self.H_T.append(temp)

                # 其余层
                else:
                    thickness = item['thickness']
                    while thickness > span:
                        z = self.H_T[-1]['z_m'] + span
                        z_b = z / b
                        _a = f_a(z_b, a/b)[0]
                        si = self.p0 / item['Es'] * (z * _a - self.H_T[-1]['z_m'] *  self.H_T[-1]['_a'])
                        temp = {'z_m': z, 'z_b': z_b, '_a': _a,
                                'Es': item['Es'], 's': si, 'A': item['Es'] * si}
                        self.H_T.append(temp)
                        thickness -= span

                        if self.H_T[-1]['s'] < 0.025 * s:
                            break
                        else:
                            s += self.H_T[-1]['s']
                            A += self.H_T[-1]['A']
                            A_Es += self.H_T[-1]['A'] / self.H_T[-1]['Es']

                    if thickness:
                        z = self.H_T[-1]['z_m'] + thickness
                        z_b = z / b
                        _a = f_a(z_b, a/b)[0]
                        si = self.p0 / item['Es'] * (z * _a - self.H_T[-1]['z_m'] *  self.H_T[-1]['_a'])
                        temp = {'z_m': z, 'z_b': z_b, '_a': _a,
                                'Es': item['Es'], 's': si, 'A': item['Es'] * si}
                        self.H_T.append(temp)

                if self.H_T[-1]['s'] < 0.025*s:
                    break
                else:
                    s += self.H_T[-1]['s']
                    A += self.H_T[-1]['A']
                    A_Es += self.H_T[-1]['A']/self.H_T[-1]['Es']


        self.s_temp = s

        self._Es = A/A_Es
        self.psai_p = get_psai_p(self._Es)
        # 最终沉降值
        self.s_final = self.psai_p*s
        return self.s_final

    '''
    确定桩数
    '''
    def confirm_num_layout(self, auto=False):
        if self.Ra == 0:
            raise ZeroDivisionError('错误: 承载力为0，查看是否已计算承载力？或者参数存在错误？')
        self.n = math.ceil((self.force['Fk'] + self.cap.calc_self_weight()) / self.Ra)
        #TODO 自动设计桩布局
        if auto:
            pass
        else:
            pass
        return self.n

    '''
    验算桩基承载力
    '''
    def check_bearing_capacity(self):
        '''单桩竖向承载力验算'''
        result = {'vertical': 0, 'horizontal': 0}
        if self.Nk < self.Ra:
            result['vertical'] = 1

        # 最大值
        if self.force['Mk'] or self.force['Hk']:
            if self.Nkmax < 1.2*self.Ra:
                pass
            else:
                result['vertical'] = 0

        '''单桩水平承载力验算'''
        if self.force['H'] < self.Rh:
            result['horizontal'] = 1

        self.check_bearing_capacity_result = result
        return result

    '''
    承台抗冲切验算
    type:: 柱下或角桩 below edge
    '''
    def check_cap_punching(self, type='below'):
        # 默认柱下抗冲切验算
        max_punching = self.cap.cap_punching_check(type=type)
        print(max_punching)
        if type=='below':
            Ft = self.force['F'] - self.N
            if Ft < max_punching:
                return 1
            else:
                return 0
        elif type=='edge':
            Nl = self.Nmax
            if Nl < max_punching:
                return 1
            else:
                return 0

    '''
    断面抗剪验算
    section:: 截面编号 int 1-一号截面 2-二号截面
    '''
    def check_shear_resist(self, section=1):
        if section == 1:
            # 承台底的角桩内边缘引 冲切线与承台顶面交点的距离 单位m
            ax = 1.4
            self.ax1 = ax
        elif section == 2:
            ax = 1.41
            self.ax2 = ax

        h0 = self.cap.thickness - self.cap.protection_thickness*1e-3
        lambda_x = ax/h0
        alpha = 1.75/(lambda_x+1)
        self.beta_hs = (800/(h0*1000))**(1/4)
        temp_1 = self.beta_hs*alpha*self.material_params['ft']*self.cap.size[0]*1000*h0
        if section == 1:
            self.shear_result1 = temp_1
        else:
            self.shear_result2 = temp_1

        V = 2*self.Nmax
        if V < temp_1:
            return 1
        else:
            return 0


    '''
    桩身配筋
    '''
    def design_pile_body(self):
        '''配置纵筋'''
        self.As = (self.N * 1e3 / 0.9 / self.varphi - self.material_params['fc'] * self.Ap * 1e6) \
                  / self.material_params['fy']
        self.temp_As = int(self.As)
        if self.As < 0:
            self.As = self.rho_min * self.Ap * 1e6
        self.vertical_steel_result = auto_steel(self.As, size=self.size)

        '''配置箍筋'''
        self.s_Asv = 150
        self.alpha_v = 0.7
        self.Asv = ((self.force['H'] * 1e3 - self.alpha_v * self.material_params['ft']
                     * self.size[0] * 1e3 * (self.size[0] * 1e3 - 2 * self.protection_thickness)) * self.s_Asv) \
                   / (self.material_params['fy'] * (self.size[0] * 1e3 - 2 * self.protection_thickness))
        self.temp_Asv = int(self.Asv)
        if self.Asv < 0:
            # 构造要求
            self.stirrup_steel_result = [150, 6]
        else:
            self.stirrup_steel_result = auto_steel(self.Asv, type='stirrup')

        return self.vertical_steel_result, self.stirrup_steel_result

    '''
    承台配筋
    '''
    def design_cap(self):
        steel_result = self.cap.cap_design(self.Nmax, self.n)
        return steel_result
















