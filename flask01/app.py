from flask import Flask

# 입구 파일을 하나 만들어줍니다.
app = Flask(__name__)

@app.route('/hello2')
def hello():
    return 'hello'