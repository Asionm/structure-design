from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import io
from dValue import *

app = Flask(__name__)
CORS(app)



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        try:
            # 读取文件内容
            string_io = io.StringIO(file.stream.read().decode("UTF-8"), newline=None)
            frame = ins(string_io)
            d_cal = D_value_method(frame)
            nodes_moment = get_nodes_moment(d_cal)
            table = get_table(d_cal)
            # 处理 frame 对象并返回所需的数据
            return jsonify({"code": 200, "data": nodes_moment,'table': table})
        except Exception as e:
            return jsonify({"code": 500, "msg": '文件格式存在问题，暂时无法处理12层以上结构！'})

if __name__ == '__main__':
    app.run(debug=True)
