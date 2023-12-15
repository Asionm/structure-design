from foundation import  Foundation
from generate import generateContent

# 创建桩基础对象
pile_foundation = Foundation()

params = {
    'column_size': (0.9, 0.88),
    'cap_materials': {
                    'concrete': 'C40',
                    'steel': 'HRB400'
                },
    'fd_materials': {
                        'concrete': 'C40',
                        'steel': 'HRB400'
                    },
    'stratigraphic_info': [
    {
        'name': '人工填土',
        'thickness': 6.25,
        'gama': 17.9,
        'c': 10,
        'phi': 6,
        'qsk': 0.001,
        'qpk': 0.001,
        'Es': 0.001
    },{
        'name': '含砾粘土',
        'thickness': 4.75,
        'gama': 18.1,
        'c': 20,
        'phi': 18,
        'qsk': 35,
        'qpk': 0.001,
        'Es': 6
    },{
        'name': '砾质粉质粘土',
        'thickness': 8.25,
        'gama': 18.5,
        'c': 25,
        'phi': 20,
        'qsk': 35,
        'qpk': 1800,
        'Es': 7
    },{
        'name': '全风化粗粒花岗岩',
        'thickness': 4.70,
        'gama': 18.6,
        'c': 26,
        'phi': 23,
        'qsk': 70,
        'qpk': 4000,
        'Es': 11
    },{
        'name': '强风化粗粒花岗岩',
        'thickness': 6.40,
        'gama': 18.9,
        'c': 28,
        'phi': 25,
        'qsk': 110,
        'qpk': 5500,
        'Es': 17
    },{
        'name': '中风化粗粒花岗岩',
        'thickness': 4.85,
        'gama': 23.0,
        'c': 30,
        'phi': 40,
        'qsk':  0.001,
        'qpk':  0.001,
        'Es': 20
    },{
        'name': '微风化粗粒花岗岩',
        'thickness': 6.10,
        'gama': 26.0,
        'c': 31,
        'phi': 65,
        'qsk':  0.001,
        'qpk':  0.001,
        'Es': 25
    },
],
    'underwater_depth': (7+10.8)/2,
    'force': {'Fk':7123,'Mk':74,'Hk':83},
    'pile_length': 19,
    'pile_size': (0.65, 0.65)
}


params_test = {
    'column_size': (0.9, 0.85),
    'cap_materials': {
                    'concrete': 'C40',
                    'steel': 'HRB500'
                },
    'fd_materials': {
                        'concrete': 'C40',
                        'steel': 'HRB500'
                    },
    'stratigraphic_info': [
    {
        'name': '素填土',
        'thickness': 5.4,
        'gama': 18.8,
        'c': 10,
        'phi': 15,
        'qsk': 0.001,
        'qpk': 0.001,
        'Es': 3
    },{
        'name': '含砾粘土',
        'thickness': 4.34,
        'gama': 18.6,
        'c': 20,
        'phi': 15,
        'qsk': 35,
        'qpk': 0.001,
        'Es': 5
    },{
        'name': '淤泥',
        'thickness': 2.3,
        'gama': 16.9,
        'c': 4,
        'phi': 6,
        'qsk': 15,
        'qpk': 0.001,
        'Es': 2.5
    },{
        'name': '粘土',
        'thickness': 2.99,
        'gama': 18.4,
        'c': 20,
        'phi': 12,
        'qsk': 20,
        'qpk': 0.0001,
        'Es': 4
    },{
        'name': '粗砂',
        'thickness': 2.09,
        'gama': 19.6,
        'c': 0,
        'phi': 25,
        'qsk': 40,
        'qpk': 0.00001,
        'Es': 7
    },{
        'name': '砾质粘土',
        'thickness': 7.89,
        'gama': 19.8,
        'c': 25,
        'phi': 22,
        'qsk':  35,
        'qpk':  1800,
        'Es': 6
    },{
        'name': '花岗岩',
        'thickness': 4.44,
        'gama': 28.0,
        'c': 28.0,
        'phi': 32,
        'qsk':  70,
        'qpk':  4000,
        'Es': 7
    },{
        'name': '花岗岩1',
        'thickness': 8.09,
        'gama': 28.0,
        'c': 35,
        'phi': 45,
        'qsk':  70,
        'qpk':  5500,
        'Es': 8
    },
],
    'underwater_depth': (7+10.8)/2,
    'force': {'Fk':7856,'Mk':78,'Hk':78},
    'pile_length': 22,
    'pile_size': (0.6, 0.6)
}

pile_foundation.auto_calc(params_test)

# 定义要填充的数据
data = {
    'foundation': pile_foundation,
}
# 生成文档
generateContent(data)


