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
      * auto 是否自动生成 布尔
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
      * size 桩截面尺寸 元组
      * auto 是否自动生成 布尔
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
      * ::xi 距离中心的距离
    * cap_punching_check
      * 作用：承台冲切验算
      * 参数说明
        * ::type 验算类型 below对应柱的向下冲切验算 edge对应角桩的冲切验算
        * ::a0x 柱边到桩内边缘距离或角桩内边缘引冲切线与承台顶面交点的水平距离 m
        * ::a0y 柱边到桩内边缘距离或角桩内边缘引 冲切线与承台顶面交点的水平距离 m
        * ::c1 角桩内边缘至承台外边缘的距离(角桩验算时） m
        * ::c2 角桩内边缘至承台外边缘的距离(角桩验算时） m