from jinja2 import Environment, FileSystemLoader

def generateContent(data):
    # 创建Jinja2环境
    env = Environment(loader=FileSystemLoader('./'))
    # 从模板文件加载模板
    template = env.get_template('template.md')

    # 使用数据渲染模板
    output = template.render(data)

    # 打印生成的Markdown内容
    print(output)

    # 将生成的Markdown内容保存到文件
    with open('output.md', 'w') as f:
        f.write(output)
