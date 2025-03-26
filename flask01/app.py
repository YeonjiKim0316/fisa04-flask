# flask run --debug --port 5001
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# flask db init
# flask db migrate
# flask db upgrade 

import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # 입구 파일을 하나 만들어줍니다.
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM을 적용
    db.init_app(app)
    migrate.init_app(app, db)

    from views import main_views, board_views
    app.register_blueprint(main_views.mbp)
    app.register_blueprint(board_views.cbp)

    return app
