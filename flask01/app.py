# flask run --debug --port 5001
from flask import Flask

def create_app():
    # 입구 파일을 하나 만들어줍니다.
    app = Flask(__name__)

    from views import main_views
    app.register_blueprint(main_views.mbp)


    return app
