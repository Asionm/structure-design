

1 设计任务
==========

1.1设计资料
-----------

  某办公楼为多层现浇钢筋混凝土框架结构，室外地坪标高同自然地面。柱网布置如图1所示，基础方案采用柱下桩基础。建筑物所处场地抗震设防烈度为7度。

![image-20230905094829505](D:\学习资料\大四\基础工程设计\code\output.assets\image-20230905094829505.png)

<p align="center">图1 某办公楼柱网布置</p>				

（1）工程及水文地质条件

  场地属滨海平原地貌类型，在勘察所揭露125.52m深度范围内的地基土属第四纪中更新Q2至全新世Q4沉积物，成因类型属滨海\~海口、浅海、溺谷、湖泽相，主要由饱和粘性土。粉性土和砂土组成，具水平层理。

  根据D2地质资料可得地基土物理力学性质指标见表1（其中层厚依据平均厚度选取）。

<p align="center">表1 地基土物理力学性质指标表</p>

| 土层编号                             | 层厚 | 土类名称 | $\gamma (kN/m^3)$ | $c(kPa)$ | $\varphi(\degree)$ | $q_{sk}$ | $q_{pk}$ | 压缩模量$Es(MPa)$ |
| ------------------------------------ | ---- | -------- | ----------------- | -------- | ------------------ | -------- | -------- | ----------------- |{% for info in foundation.stratigraphic_info %}
| {{loop.index}} | {{info['thickness']}} | {{info['name']}} | {{info['gama']}} | {{info['c']}} | {{info['phi']}} | {{info['qsk']|float|round(2)}} | {{info['qpk']|float|round(2)}} | {{info['Es']|float|round(2)}}|{% endfor %}

  地下水类型及地下水位：拟建场地的地下水类型主要为潜水以及承压水。潜水位埋深随季节、气候等因素而有所变化。勘察期间测得地下水埋深约{{ underwater_depth }}m，地下水对混凝土无侵蚀性。

（3）已知柱KZ2截面尺寸为{{ foundation.cap.column_size[0]*1000 }} mm x {{ foundation.cap.column_size[1]*1000 }} mm，上部结构作用在柱KZ2底部的荷载标准组合见表2，设计中永久荷载效应起控制作用。表中弯矩、水平力均为横向方向。

<p align="center">表2 柱底荷载效应标准组合值</p>

  | 竖向力(kN)                      | 弯矩($kN \cdot m$)             | 水平力(kN)                      |
|------------------------------|------------------------------|------------------------------|
| {{ foundation.force['Fk'] }} | {{ foundation.force['Mk'] }} | {{ foundation.force['Hk'] }} |

1.2设计要求
-----------

  设计柱KZ2下的桩基础，设计内容包括：

（1）根据已知条件选择桩的类型、材料（混凝土等级）和几何尺寸（截面尺寸和桩长）

（2）选定承台的埋深；

（3）确定单桩竖向（和水平向）承载力设计值（可按规范经验公式法确定）；

（4）确定桩的数量、间距和布桩方式（按单桩承载力计算所需桩数，按基本构造要求、布桩原则进行布桩）；

（5）设计承台平面尺寸（按照桩的平面布置方式和桩边距等构造要求确定承台的平面形状和尺寸）；

（6）验算桩基的承载力和沉降；

（7）桩身结构设计（内力计算、配筋，构造设计）；

（8）承台设计（承台抗冲切验算和承台抗剪验算）；

（9）绘制桩基施工图（桩基础平面布置图、桩基础剖面图、承台配筋图、桩身配筋图、桩与承台连接详图）。

2 选择桩的类型、材料和几何尺寸
==============================

2.1 确定桩类型
--------------

  由于上部土层均为粘性土层，且考虑到成本问题，桩类型选择为挤土桩。由于地层底部存在岩石，因此桩类型为端承桩。在桩的截面类型上，选择常见的预制混凝土方形桩。（规范P7-8）

2.2 确定材料
------------

  混凝土等级选用{{ foundation.materials['concrete'] }}，钢筋为{{ foundation.materials['steel'] }}，则$E_c={{ foundation.material_params['Ec'] }}N/mm^2$，$f_y={{foundation.material_params['fy']}}N/mm^2$，$f_c={{foundation.material_params['fc']}}N/mm^2$。

2.3 确定桩的几何尺寸
--------------------

  根据土层参数、柱截面尺寸与荷载标准组合值，由于第3层粘聚力较大，所以初步考虑第
3 层的砾质粉质粘土为桩端持力层。桩截面尺寸选定为{{foundation.size[0]*1000}}mm$\times${{foundation.size[1]*1000}}mm，桩长 {{ pile_length }}m，桩端进入持力层8m，承台埋深 {{ cap_depth }}m。

3 单桩承载力计算
================

3.1 计算单桩竖向承载力特征值
----------------------------

计算单桩竖向承载力特征值如下所示，
$$
A_p={{foundation.size[0]}}\times{{foundation.size[1]}}={{ foundation.Ap|float|round(2) }}m^2
$$

$$
u={{foundation.size[0]}}\times4={{ foundation.u }}m
$$

$$
Q_{uk}=q_{pk}A_p+u\sum{q_{sik}l_i}={{ foundation.qpk }}\times{{ foundation.Ap|float|round(2) }}+{{ foundation.u }}\times({% for qsk in foundation.qsk_li %}{% if loop.index==1 %}{{qsk|float|round(2)}}{% else %}+{{qsk|float|round(2)}}{% endif %}{% endfor %})={{ foundation.Quk|float|round(2) }}kN
$$

$$
R_a=\frac{Q_{uk}}{2}=\frac{ {{ foundation.Quk|float|round(2) }} }{2}={{ foundation.Ra|float|round(2) }}kN
$$

因此单桩承载力特征值为{{ foundation.Ra|float|round(2) }}kN。

3.2 计算单桩水平承载力特征值
----------------------------

  根据《建筑桩基技术规范》5.7节可得单桩水平承载力特征值计算过程如下。

预制桩的单桩水平承载力特征值计算公式为：

1.  计算桩身抗弯刚度：

  查《混凝土结构设计规范GB50010-2010》规范附表得，由于混凝土强度为{{foundation.materials['concrete']}}，钢筋为{{foundation.materials['steel']}}，保护层厚度取{{foundation.protection_thickness}}mm，配筋率假设为$\rho_g={{ foundation.rho_g }}$，因此桩身换算截面受拉边缘的截面模量为：
$$
W_0=\frac{b}{6}[b^2+2(\alpha_E-1)\rho_gb_0^2]\\
=\frac{ {{foundation.size[0]}} }{6}\times[{{foundation.size[0]}}^2+2\times(\frac{ {{foundation.material_params['Es']}} }{ {{foundation.material_params['Ec']}} }-1)\times{{foundation.rho_g}}\times( {{ foundation.size[0] }} - 2 \times {{ foundation.protection_thickness }})]\\
={{ foundation.W0|float|round(0) }}mm^2
$$

  那么桩身抗弯刚度为：
$$
EI=0.85E_cI_0=0.85E_c\frac{W_0b_0}{2}\\
=0.85\times{{ foundation.material_params['Ec'] }}\times\frac{ {{ foundation.W0 }} \times ( {{ foundation.size[0]*1000 }}  - {{ 2 * foundation.protection_thickness}})}{2}\\
={{ foundation.EI|float|round(0) }}
$$

2. 计算桩的水平变形系数:

由于$b<1m$，所以桩身的计算宽度：
$$
b_0=1.5b+b=1.5\times{{foundation.size[0]}}+0.5={{1.5*foundation.size[0]+0.5}}m
$$
  由于桩侧面由多种土组成，所以根据规范《建筑桩基技术规范2008》表5.7.5，（https://baijiahao.baidu.com/s?id=1762253040280708770&wfr=spider&for=pc）需要计算主要影响深度$h_m$，
$$
h_m=2(b+1)=2\times({{foundation.size[0]}}+1)={{2*(foundation.size[0]+1)}}m
$$
  该深度范围内地基土为松散土，取比例系数$m={{foundation.m}}MN/m^4$ 。

  所以计算桩的水平变形系数为：
$$
\alpha=\sqrt[5]{\frac{mb_0}{EI}}={{foundation.alpha|float|round(2)}}
$$

3. 确定桩顶（承台）的水平位移允许值$x_{0a}={{foundation.x0a}}mm$

4. 确定桩顶水平位移系数

   桩的换算埋深 $\alpha h={{ foundation.alpha_h }}$，因此$v_x={{foundation.vx}}$。

将数据带入式子可得，$R_{ha}={{foundation.Rha|float|round(2)}}kN$

5. 考虑群桩效应

  https://mp.weixin.qq.com/s/sEa7cnb4G06yWLYRiF9LkA

  桩中心距为$s_a = {{ foundation.sa }}m$，由于$\frac{s_a}{b}={{(foundation.sa/foundation.size[0])|float|round(2)}}$, 且考虑地震作用，所以群桩效应综合系数公式为：
$$
\eta_h=\eta_i\eta_r+\eta_l
$$
  假设桩数为{{ foundation.n }}根，那么沿水平荷载方向与垂直荷载方向每排桩的桩数分别为，$n_1 = {{ foundation.eta1 }}$, $n_2={{foundation.eta2}}$, 所以：
$$
\eta_i=\frac{(\frac{s_a}{d})^{0.015\eta_2+0.45}}{0.15n_1+0.10n_2+1.9}\\
={{ foundation.eta_i|float|round(2) }}
$$
  查表得$\eta_r={{foundation.eta_r}}$，

  承台侧向土抗力效应系数为：
$$
\eta_l=\frac{mx_{0a}B_c^{'}h_c^{2}}{2n_1n_2R_{ha}}={{ foundation.eta_l|float|round(2) }}
$$
  因此群桩效应综合系数为$\eta_h=\eta_i\eta_r+\eta_l={{foundation.eta_h|float|round(2)}}$，

  那么$R_h=\eta_hR_{ha}={{ foundation.Rh|float|round(2) }}kN$

4 初步确定桩数量及承台尺寸
==========================

  假设承台尺寸为${{ foundation.cap.size[0] }}m\times{{ foundation.cap.size[1] }}m$，厚度为${{foundation.cap.thickness}}m$，埋深${{foundation.cap.depth}}m$，承台及其上土平均重度为*20kN/m3*，则承台及其上土自重的标准值为：
$$
G_k=20\times{{foundation.cap.size[0]}}\times{{foundation.cap.size[1]}}\times\times{{foundation.cap.depth}}={{foundation.cap.weight}}kN
$$
  因此可取{{foundation.n}}根桩。承台的平面尺寸仍取为，如下图所示。



<p align="center">图 桩的布置及承台尺寸</p>	

5 验算桩基承载力
=================

5.1 单桩竖向承载力验算
----------------------

  由式（12）得$G_k={{foundation.cap.weight}}kN$，则单桩的平均竖向力为：
$$
N_k=\frac{F_k+G_k}{n}={{foundation.Nk|float|round(2)}}kN{% if foundation.Nk<foundation.Ra %}<R_a{% else %}>R_a{% endif %}
$$
  {% if foundation.Nk<foundation.Ra %}符合要求。{% else %}不符合要求。{% endif %}

  计算单桩偏心荷载下最大竖向力为：
$$
N_{k,max}=\frac{F_k+G_k}{n}+\frac{M_yx_i}{\sum{x_j^2}}={{foundation.Nkmax|float|round(2)}}kN{% if foundation.Nkmax<1.2*foundation.Ra %}<1.2R_a{%else%}\geq 1.2R_a{%endif%}
$$
  {% if foundation.Nkmax<1.2*foundation.Ra %}符合要求。{% else %}不符合要求。{% endif %}

5.2单桩水平承载力验算
---------------------

  考虑群桩效应后的单桩水平承载力特征值为：$R_h={{foundation.Rh|float|round(2)}}kN$，

  水平荷载设计值为：$H=1.35H_k={{foundation.force['H']|float|round(2)}}kN{%if foundation.force['H']<foundation.Rh%}<R_h{%else%}\geq R_h{%endif%}$，所以{%if foundation.force['H']<foundation.Rh%}通过{%else%}不通过{%endif%}群桩基础中的单桩承载力验算。

6 桩身结构设计
==============

6.1 计算荷载设计值
------------------

$$
F=1.35F_k=1.35\times{{foundation.force['Fk']}}={{foundation.force['F']|float|round(2)}}kN\\
M=1.35M_k=1.35\times{{foundation.force['Mk']}}={{foundation.force['M']|float|round(2)}}kN\cdot m\\
H=1.35H_k=1.35\times{{foundation.force['H_k']}}={{foundation.force['H']|float|round(2)}}kN
$$

6.2 配置桩身纵筋
----------------

  由上面的计算可得桩截面面积$A_p={{foundation.Ap|float|round(2)}}m^2$，又查表得{{foundation.materials['steel']}}钢筋的抗拉强度为$f_y={{foundation.material_params['fy']}}N/mm^2$，{{foundation.materials['concrete']}}混凝土的强度设计值为$f_c={{foundation.material_params['fc']}}N/mm^2$，而每根桩的设计竖向承载力*N*为：
$$
N=\frac{F}{n}={{foundation.N|float|round(2)}}kN
$$
  钢筋混凝土轴心受压构件的正截面受压承载力应符合下列规定：
$$
N\leq0.9\varphi(f_cA_p+f_yA_s)
$$
  又由于由规范5.8.4条，取桩基的稳定系数$\varphi$为：
$$
\varphi={{foundation.varphi}}
$$
  那么钢筋的截面积$A_s$为：
$$
A_s=\frac{\frac{N}{0.9\varphi}-f_cA}{f_y}={{foundation.temp_As}}{% if foundation.temp_As<0 %}<0{%else%}>0{%endif%}
$$
  {% if foundation.temp_As<0 %}所以按照构造要求配筋，依据规范4.1.6条最小配筋率不小于0.8%，所以取$\rho={{foundation.rho_min}}$，则：
$$
A_s=\rho A={{foundation.As}}
$$
{%else%}查表得:{%endif%}

  选用{{foundation.vertical_steel_result[0]}}根{{foundation.vertical_steel_result[1]}}*mm*钢筋，$A_s={{foundation.vertical_steel_result[0]*3.14*foundation.vertical_steel_result[1]**2/4}}mm^2$。

6.3 配置桩身箍筋
----------------

  受弯构件的斜截面受剪承载力应符合以下规定：
$$
V_{cs}=\alpha_{cv}f_tbh_0+f_{yv}\frac{A_{sv}}{s}h_0
$$
  其中：

  每根桩斜截面上混凝土和箍筋的受剪承载力设计值为：
$$
V_{cs}=H={{foundation.force['H']|float|round(2)}}kN
$$
  截面混凝土受剪承载力系数为：
$$
\alpha_{cv}={{foundation.alpha_v}}
$$
  计算高度为：
$$
h_0={{foundation.size[0]*1e3-2*foundation.protection_thickness}}mm
$$
  暂取箍筋间距为150mm，即：
$$
s=150mm
$$
  则箍筋面积为：
$$
A_{sv}=\frac{(V_{cs}-\alpha_{cv}f_tbh_0)s}{f_{yv}h_0}={{foundation.temp_Asv}} {% if foundation.temp_Asv<0 %}<0{%else%}>0{%endif%}
$$
  因此{% if foundation.temp_Asv<0 %}按照构造要求配置箍筋。{%else%}{%endif%}箍筋加密区选用$\varphi ${{ foundation.stirrup_steel_result[1] }}@{{ foundation.stirrup_steel_result[0] }}箍筋，非加密区选用$\varphi ${{ foundation.stirrup_steel_result[1] }}@{{ foundation.stirrup_steel_result[0] }}箍筋。

7 承台设计
==========

  对于承台进一步设计为：取承台厚 {{foundation.cap.thickness}}m，下设厚度 100mm，使用强度等级为 C10的混凝土垫层，保护层为{{foundation.cap.protection_thickness}}mm，则$h_0 = {{foundation.cap.thickness-foundation.cap.protection_thickness*1e-3}}$ m；混凝土强度为{{foundation.materials['concrete']}}，混凝土抗拉强度为$ f_t = {{foundation.material_params['ft']}}N/mm^2$，钢筋选用{{foundation.materials['steel']}}级，钢筋抗拉强度设计值为$ f_y = {{foundation.material_params['fy']}} N/mm^2$，承台设计计算图如下所示。



<p align="center">图 承台设计计算图</p>

  各桩不计承台以及其上土重 $G_k$ 的净反力。

  由式（20）得各桩平均竖向力为：$N={{foundation.N|float|round(2)}}kN$，

  最大竖向力为：
$$
N_{max}=1.35(\frac{F_k}{n}+\frac{M_yx_i}{\sum{x_j^2}})={{foundation.Nmax|float|round(2)}}{% if foundation.Nmax<1.2*foundation.Ra %}<1.2R_a{%else%}\geq1.2R_a{%endif%}
$$
  对于I—I 断面：
$$
M_y=\sum{N_ix_i}=2N_{max}x_i={{(2*foundation.Nmax*foundation.cap.xi)|float|round(2)}}kN\cdot m
$$
  钢筋面积：
$$
A_s=\frac{M_y}{0.9f_yh_0}={{foundation.cap.As|float|round(2)}}mm^2
$$
  选用{{ foundation.cap.vertical_steel_result[0] }}根{{ foundation.cap.vertical_steel_result[1] |float|round(2)}}mm钢筋，$A_s={{ (foundation.cap.vertical_steel_result[0]*3.14*foundation.cap.vertical_steel_result[1]**2/4)|float|round(2) }}mm^2$，平行于x轴布置。对于II—II 断面由于对称性，所以可知其钢筋配置与I—I断面一致，选用{{ foundation.cap.vertical_steel_result[0] }}根{{ foundation.cap.vertical_steel_result[1] }}mm钢筋，平行y轴布置。

8 承台抗冲切验算
=================

8.1 柱的向下冲切验算
--------------------

  柱的向下冲切验算涉及到的计算参数如下：

  承台混凝土抗拉强度设计值：$f_t={{foundation.material_params['ft']}}kN/mm^2$

  柱截面边长：$a_c={{foundation.cap.column_size[0]*1e3}}mm, b_c={{foundation.cap.column_size[1]*1e3}}mm$

  两个方向的柱边或变阶处至相应桩内边缘的水平距离为：
$$
a_{0x}={{foundation.cap.a0x|float|round(2)}}m\\
a_{0y}={{foundation.cap.a0y|float|round(2)}}m
$$


  由几何关系得到的$a_{0x}$和$a_{0y}$均满足冲切验算参数要求（即$0.2h_0<a_{0x}(a_{0y})<h_0)$），因此不作修正。

  两个方向的冲跨比为：
$$
\lambda_{0x}=\frac{a_{0x}}{h_0}={{ foundation.cap.lambda_0x|float|round(2) }}\\
\lambda_{0y}=\frac{a_{0y}}{h_0}={{ foundation.cap.lambda_0y|float|round(2) }}
$$


  $\lambda_{0x}$和 $\lambda_{0y}$均满足0.2\~1.0的取值要求。

  冲切系数为：
$$
\beta_{0x}=\frac{0.84}{\lambda_{0x}+0.2}={{foundation.cap.beta_0x|float|round(2)}}\\
\beta_{0y}=\frac{0.84}{\lambda_{0y}+0.2}={{foundation.cap.beta_0y|float|round(2)}}
$$
  由于$h_0={{foundation.cap.thickness*1000-foundation.cap.protection_thickness}}$，经过插值获得的截面高度影响系数为（书P71）：
$$
\beta_{hp}={{foundation.cap.beta_hp|float|round(2)}}
$$
  开始进行柱的向下抗冲切验算。

  该承台可以接受的最大冲切力为：
$$
2[\beta_{0x}(b_c+a_{0y})+\beta_{0y}(a_c+a_{0x})]\beta_{hp}f_th_0={{foundation.cap.max_punching_below|float|round(2)}}kN
$$
   基本组合下柱根部轴力设计值$F={{foundation.force['F']}}kN$，每根桩的设计竖向承载力为$N={{foundation.N}}$，所以其冲切设计值为：
$$
F_t=F-N={{(foundation.force['F']-foundation.N)|float|round(2)}}kN{% if (foundation.force['F']-foundation.N)<foundation.cap.max_punching_below %}<{{foundation.cap.max_punching_below}}kN{% else %}\geq{{foundation.cap.max_punching_below}}kN{%endif%}
$$
  综上所述，该承台{% if (foundation.force['F']-foundation.N)<foundation.cap.max_punching_below %}通过{% else %}不通过{%endif%}柱的向下冲切验算。

8.2 角桩的冲切验算
------------------

  角桩冲切验算涉及到的计算参数如下：

  两个方向上从角桩内边缘至承台外边缘的距离为：
$$
c_1=c_2={{(foundation.cap.c1/1000)|float|round(2)}}m
$$
  两个方向上从承台底的角桩内边缘引冲切线与承台顶面交点的水平距离为：
$$
a_{1x}={{foundation.cap.a0x|float|round(2)}}m\\
a_{1y}={{foundation.cap.a0x|float|round(2)}}m
$$
  两个方向上的角桩冲切系数：
$$
\lambda_{1x}=\frac{a_{1x}}{h_0}={{ foundation.cap.lambda_0x|float|round(2) }}\\
\lambda_{1y}=\frac{a_{1y}}{h_0}={{ foundation.cap.lambda_0y|float|round(2) }}
$$
  两个方向上的角桩冲切系数：
$$
\beta_{1x}=\frac{0.56}{\lambda_{1x}+0.2}={{foundation.cap.beta_1x|float|round(2)}}\\
\beta_{1y}=\frac{0.56}{\lambda_{1y}+0.2}={{foundation.cap.beta_1y|float|round(2)}}
$$
  由于$h_0={{foundation.cap.thickness*1000-foundation.cap.protection_thickness}}$，经插值获得的截面高度影响系数为：
$$
\beta_{hp}={{foundation.cap.beta_hp|float|round(2)}}
$$
  开始进行角桩抗冲切验算。

  角桩桩顶相应于作用基本组合时的竖向力设计值为：
$$
N_l=N_{max}={{foundation.Nmax|float|round(2)}}kN
$$
  抗冲切力为：
$$
[\beta_{1x}(c_2+\frac{a_{1y}}{2})+\beta_{1y}(c_1+\frac{a_{1x}}{2})]\beta_{hp}f_th_0={{foundation.cap.max_punching_edge|float|round(2)}}kN{% if foundation.cap.max_punching_edge>foundation.Nmax %}>{{foundation.Nmax|float|round(2)}}kN{% else %}\leq{{foundation.Nmax|float|round(2)}}kN{%endif%}
$$
  则该承台{% if foundation.cap.max_punching_edge>foundation.Nmax %}满足{% else %}不满足{%endif%}角桩的冲切验算。

9 承台抗剪验算
=============

9.1 I—I 断面抗剪验算
--------------------

  从承台底的角桩内边缘引$45\degree$冲切线与承台顶面交点的距离为：
$$
a_x={{foundation.ax1}}m
$$
  计算截面的剪跨比为：
$$
\lambda_x=\frac{a_x}{h_0}={{(foundation.ax1/(foundation.cap.thickness - foundation.cap.protection_thickness*1e-3))|float|round(3)}}
$$
  剪切系数为：
$$
\alpha=\frac{1.75}{\lambda_x+1}={{(1.75/((foundation.ax1/(foundation.cap.thickness - foundation.cap.protection_thickness*1e-3))+1))|float|round(3)}}
$$
  受剪切承载力截面高度的影响系数为：
$$
\beta_{hs}=(\frac{800}{h_0})^{\frac{1}{4}}={{foundation.beta_hs|float|round(3)}}
$$
  则：
$$
V=2N_{max}={{(2*foundation.Nmax)|float|round(2)}}kN\\
\beta_{hs}\alpha f_t bh_0={{foundation.shear_result1|float|round(3)}}{% if foundation.shear_result1>2*foundation.Nmax %}>{{(2*foundation.Nmax)|float|round(2)}}kN{%else%}\leq {{(2*foundation.Nmax)|float|round(2)}}kN{%endif%}
$$
  因此I—I 断面{% if foundation.shear_result1>2*foundation.Nmax %}通过{%else%}不通过{%endif%}验算。

9.2 II—II断面抗剪验算
---------------------

  从承台底的角桩内边缘引$45\degree$冲切线与承台顶面交点的距离为：
$$
a_x={{foundation.ax2|float|round(2)}}m
$$
  计算截面的剪跨比为：
$$
\lambda_x=\frac{a_x}{h_0}={{(foundation.ax2/(foundation.cap.thickness - foundation.cap.protection_thickness*1e-3))|float|round(3)}}
$$
剪切系数为：
$$
\alpha=\frac{1.75}{\lambda_x+1}={{(1.75/((foundation.ax2/(foundation.cap.thickness - foundation.cap.protection_thickness*1e-3))+1))|float|round(3)}}
$$
受剪切承载力截面高度的影响系数为：
$$
\beta_{hs}=(\frac{800}{h_0})^{\frac{1}{4}}={{foundation.beta_hs|float|round(2)}}
$$
则：
$$
V=2N_{max}={{(2*foundation.Nmax)|float|round(2)|float|round(2)}}kN\\
\beta_{hs}\alpha f_t bh_0={{foundation.shear_result2|float|round(2)}}{% if foundation.shear_result2>2*foundation.Nmax %}>{{(2*foundation.Nmax)|float|round(2)}}kN{%else%}\leq {{(2*foundation.Nmax)|float|round(2)}}kN{%endif%}
$$
因此II—II断面{% if foundation.shear_result2>2*foundation.Nmax %}通过{%else%}不通过{%endif%}验算。

10 沉降计算
===========

  本设计采用实体深基础计算方法计算中心点沉降。计算桩端平面处的附加压力涉及到的参数如下：

  承台尺寸为：
$$
a=b={{foundation.cap.size[0]}}m
$$
  群桩的外缘矩形面积的长、短边的长度：
$$
a_0=b_0={{foundation.cap.size[0]-1}}m
$$
  桩入土深度：
$$
l={{foundation.length}}
$$
  桩所穿越土层的内摩擦角加权平均值为：
$$
\bar\varphi={{foundation._varphi|float|round(2)}}\degree
$$
  竖向力为$F={{foundation.force['F']}}kN$，承台自重$G_k={{foundation.cap.weight}}kN$，承台底面高层处地基土的自重压力为：
$$
p_{c0}=\gamma h={{ foundation.pc0|float|round(2) }}kPa
$$
  则桩端平面处的附加压力为：
$$
p_0=\frac{F+G-p_{c0}ab}{(b+2ltan\frac{\bar\varphi}{4})(a_0+2ltan\frac{\bar\varphi}{4})}={{foundation.p0|float|round(2)}}kPa
$$
桩基最终计算沉降量*s*涉及到的参数如下：

  基础承台的长宽比为：
$$
\frac{a}{b}=1
$$


  地基计算变形量为：
$$
s^{'}_i=\sum{\frac{p_0}{E_{si}}}(z_i\bar a_i-z_{i-1}\bar a_{i-1})
$$
<p align='center'>图 桩的布置及承台尺寸</p>



| z/m  | z/b  | $\bar a_i$ | $E_s$ | $s^{'}$ | $A_i$ |
| ---- | ---- | ---- | ---- | ---- | ---- |{% for item in foundation.H_T %}
| {{item['z_m']|float|round(2)}} | {{item['z_b']|float|round(2)}} | {{item['_a']|float|round(2)}} | {{item['Es']}} | {{item['s']|float|round(2)}} | {{item['A']|float|round(2)}} |{% endfor %}

  查表得，地基计算最终变形量为：

$$
\sum^n_{i=1}{s^{'}_i}={{foundation.s_temp|float|round(2)}}mm
$$

$$
\Delta_{sn}={{foundation.H_T[-1]['s']|float|round(2)}}mm<0.025\sum^n_{i=1}{s^{'}_i}
$$

  变形计算深度范围内压缩模量的当量值为：

$$
\bar E_s=\frac{\sum{A_i}}{\sum{\frac{A_i}{E_{si}}}}={{foundation._Es|float|round(2)}}Mpa\leq15MPa
$$
  查表得到桩基沉降计算经验系数为：

$$
\phi _p={{foundation.psai_p}}
$$
  则桩基最终计算沉降量为：
$$
s=\phi _p\sum^n_{i=1}{s^{'}_i}={{foundation.s_final|float|round(2)}}mm
$$


11 施工图绘制
=============

11.1 地层分布图
---------------

11.2 基及土层分布示意图
-----------------------

11.3 平面布置图
---------------

11.4 柱对承台冲切验算示意图
---------------------------

11.5 角桩对承台冲切验算示意图
-----------------------------

11.6 承台斜截面受剪计算示意图
-----------------------------

11.7 承台受弯计算示意图
-----------------------

11.8 承台配筋图
---------------

11.9 桩配筋图
-------------
