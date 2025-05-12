# coding=utf-8
# 导入Flask类
from flask import Flask, jsonify

# Flask 接收一个参数__name__，当前模块的文件名
# Flask 在查找静态文件，或者模板时候默认以当前文件所在的目录去查找
# 如果传一个不存在的模块名，将默认使用当前文件
app = Flask(__name__)


# 装饰器将路由映射到视图index
@app.route('/')
def index():
    return jsonify([
        {
            'name': 'jiaoxingk',
            'status': "有库存"
        },
        {
            'name': 'haha',
            'status': "有东西"
        },
        {
            'name': 'haha1',
            'status': "有东西"
        },
        {
            'name': 'haha2',
            'status': "有东西"
        },
    ])


if __name__ == '__main__':
    # Flask 应用程序实例的方法run启动web服务器
    app.run(debug=True)
