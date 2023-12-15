## 框架结构设计

### 矩阵位移法计算

源码位于`frame_structure\matrix_displacement_method`

### opensees验证

源码位于`frame_structure\opensees_code`

### D值法自动化计算与可视化

**源码位置**

* 计算源码位于`frame_structure\D_value_code`
* 网页可视化服务端源码位于`frame_structure\flask-server`
* 客户端源码位于`frame_structure\web-site`

**介绍**

为了体现“智能建造课程设计VI-框架结构设计”中的智能性，次程序主要讨论编程的思想实现简单结构下D值法的自动计算，作为课程设计的拓展部分。

（1）D值法手算存在的问题

在D值法的计算中，涉及到的流程如图下所示，主要可以概括为三个核心步骤。首先是D值的计算，该计算过程中涉及到的侧移刚度修正系数的求解，这需要进行复杂且繁琐的计算。第二步是确定反弯点的位置，这一步骤需要参考多个表格，而这些表格往往有着各种不同的规则。最后一步是计算弯矩值，这一步涉及到重复而复杂的迭代计算。因此，手动进行D值法计算将会是一个十分繁杂的过程。在工程实践中，我们通常只关注最终的分析结果，而计算过程本身却可能耗费大量的时间和精力。若能使用自动化的程序对D值法这些重复的步骤进行计算，将会大大节省时间并将精力集中于分析受力结果。

![img](https://github.com/Asionm/structure-design/blob/main/README.assets/clip_image002.png)

（2）编程实现D值法计算

计算所使用的编程语言为Python，程序的处理流程如下图所示。该流程首先涉及到将模型的几何结构、受力信息以及材料截面等信息写入系统。接着，这些信息以类和对象的形式存储，其中包括节点与杆件的详细信息以及它们之间的空间关系。随后，系统载入包含反弯点数据的json文件，并执行插值操作以便于后续使用。基于节点的空间信息，系统遍历计算出每个节点的𝛼𝑐值。然后，利用楼层信息和i值来确定反弯点的高度比v。接下来，系统计算D值，然后计算每个反弯点处的剪力Vim。有了这些数据，系统进一步计算出各个节点的弯矩值。最后，利用这些计算结果绘制出弯矩图，为结构分析提供直观的视图。

![img](https://github.com/Asionm/structure-design/blob/main/README.assets/clip_image002-17024619459071.png)

**可视化网页程序**

演示网页位于：https://asionm.github.io/structure-design/

![demo](https://github.com/Asionm/structure-design/blob/main/README.assets/demo.gif)

*注意：程序尚未完善，因此只能输入简单的结构与受力情况，且层数不能超过12层。*

## 基础工程设计

### 简介

此程序主要依据规范以及一些一般的土力学计算公式实现对简单基础的设计，并生成对应的计算书。其中计算书主要生成为markdown格式，使用的编程语言为python语言。主要代码位于: `foundation_design\calculate_code`

### 程序结构

#### 文件树

│  appendix.py（存储了附录的一些数据包含混凝土弹模、抗拉强度设计值等）
│  cap.py （承台类）
│  foundation.py（桩基础类）
│  generate.py（生成计算书）
│  main.py（入口文件，启动文件）
│  output.md（输出的计算书）
│  template.md（渲染模板）
│  tools.py（一些工具函数）
│
└─output.assets（计算书中的一些图片）
        image-20230905094829505.png

#### 程序执行流程

![程序流程](https://github.com/Asionm/structure-design/blob/main/README.assets/程序流程.svg)

#### 部分api接口介绍

* Foundation：桩基础类，里面包含了桩基的一些基本信息与计算方法。
  * auto_calc：接收一些设计参数并调用对应的函数实现完整的简单基础设计
  * register_stratigraphic_info
    * 作用：初始化地层信息
    * 参数说明：
      * stratigraphic_info：完整的地层信息，类型为对象列表。
  * add_stratigraphic_info
    * 作用：添加地层信息
    * 参数说明：
      * info：为要添加的地层信息，顺延添加。类型为字典。
  * remove_stratigraphic_info
    * 作用：去除地层信息
    * 参数说明
      * index 需要去除的地层索引，默认为-1即默认去除最后一个地层。
      * all 是否去除所有地层，默认为0即不去除所有，若为1则去除所有。
  * register_hydrologic_info
    * 作用：注册水文信息
    * 参数说明
      * depth 地下水深度，浮点数。
  * register_fd_params
    * 作用：注册基础参数
    * 参数说明
      * length 桩长 浮点数
      * size 桩截面尺寸 元组
      *  auto 是否自动生成 布尔
  * register_force_params
    * 作用：注册受力信息
    * 参数说明
      * force 受力 字典、
  * register_material_params
    * 作用：注册材料信息
    * 参数说明：
      * material_params 材料信息 字典
  * calc_bearing_capacity
    * 作用：单桩承载力计算
    * 参数说明
      *  sa 桩中心距
  * calc_settlement
    * 作用：沉降计算
    * 参数说明
      * 仅使用实体深基础中的荷载扩散法进行计算
  * confirm_num_layout
    * 作用：确定桩数
    * 参数说明：
      * auto 是否自动确定
  * check_bearing_capacity
    * 作用：验算桩基承载力
    * 参数说明
  * check_cap_punching
    * 作用：承台抗冲切验算
    * 参数说明
      * type:: 柱下或角桩 below edge
  * check_shear_resist
    * 作用：断面抗剪验算
    * 参数说明
      * section 截面编号 int 1-一号截面 2-二号截面
  * design_pile_body
    * 作用：桩身配筋
  * design_cap
    * 作用：承台配筋
* Cap：承台类，包含承台设计的一些信息与计算方法，被包含在foundation对象中。
  * register_column
    * 作用：注册柱子参数
    * 参数说明
      * size 桩截面尺寸 元组
  * register_cap
    * 作用：注册承台参数    
    * 参数说明
      * depth 桩长 浮点数
      *  size 桩截面尺寸 元组
      *  auto 是否自动生成 布尔
  * register_material_params
    * 作用：注册材料信息
    * 参数说明
      * material_params 材料信息 字典
  * calc_self_weight
    * 作用：计算承台自重
  * cap_design
    * 作用：承台配筋设计
    * 参数说明
      * ::Nmax
      * ::n
      * ::protection_thickness 保护层厚度
      *  ::xi 距离中心的距离
    * cap_punching_check
      * 作用：承台冲切验算
      * 参数说明
        * ::type 验算类型 below对应柱的向下冲切验算 edge对应角桩的冲切验算
        *  ::a0x 柱边到桩内边缘距离或角桩内边缘引冲切线与承台顶面交点的水平距离 m
        *  ::a0y 柱边到桩内边缘距离或角桩内边缘引 冲切线与承台顶面交点的水平距离 m
        * ::c1 角桩内边缘至承台外边缘的距离(角桩验算时） m
        *  ::c2 角桩内边缘至承台外边缘的距离(角桩验算时） m



### TODO  

**计算程序**  

- [x] 基本计算  
- [x] 报告生成  
- [ ] 适配各种情况

**自动绘图**

**可视化网页** 

- [ ] 页面搭建
- [ ] 连接计算程序
