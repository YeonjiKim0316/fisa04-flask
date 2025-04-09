# flask run --debug --port 5001
from flask import Flask, request, g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import config
# flask db init
# flask db migrate
# flask db upgrade 


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def create_app():
    app= Flask(__name__)
    app.config.from_object(config)
    
    
    # 모든 요청 전 처리 (비즈니스 로직 외 인증 등의 부가 로직)
    @app.before_request
    def get_client_ip():
        g.client_ip = request.remote_addr or "unknown"  # g 객체에 client_ip 저장
        

    # Logging
    import logging.config
    import os
    import datetime

		
    # logs 디렉터리 생성
    logs_dir = os.path.join(app.root_path, 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)  


    today_date = datetime.datetime.now().strftime("%Y-%m-%d")  
    # if not app.debug: 
    if app.debug: 
        # 즉 debug=true면 이는 false로서 아래 코드를 읽어옵니다.
        # 실제 상용화단계에서 로깅을 진행하라는 의미입니다.
            import logging
            # pip install python-json-logger 
            from pythonjsonlogger import jsonlogger  

            logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {  # 로그 출력 패턴 1
                    'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                    'style': '{',
                },
                'simple': { # 로그 출력 패턴 2
                    'format': '{levelname} {message}',
                    'style': '{',
                },
                'json-format': {  # JSON 형식의 로그 포맷터
                    '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                    'format': '%(levelname)s %(asctime)s %(name)s %(message)s',
                },

            },
            'handlers': {
                'console': { # 콘솔에 출력하는 로그의 범위
                    'level': 'INFO',
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose',
                },
                'file': {
                    'level': 'DEBUG',
                    'encoding': 'utf-8',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': app.root_path + f'/logs/{today_date}-mysiteLog.log', # 이 파일에 로그를 수집할 예정
                    'formatter': 'json-format', # 적용시킨 로그 출력 패턴 1대로 수집
                    # 'maxBytes': 1024*1024*5, # 5 MB
                    'maxBytes': 1024*1, # 1 B
                    'backupCount': 5,
                },
                'errors': { # 에러가 난 경우 별도 파일로 수집할 예정
                    'level': 'ERROR',
					'encoding': 'utf-8',
                    'class': 'logging.FileHandler',
                    'filename': app.root_path + f'/logs/{today_date}-mysiteErrorLog.log', # logs 폴더 생성 필요
                    'formatter': 'simple', # 로그 출력 패턴 2대로 수집
                },
            },
            'loggers': {
                'flask.app': {  
                    'handlers': ['console', 'file'],
                    'level': 'DEBUG',
                    'propagate': True,
                },
                'flask.request': {
                    'handlers': ['errors'],
                    'level': 'ERROR',
                    'propagate': True,
                },
                'my': {
                    'handlers': ['console', 'file', 'errors'],
                    'level': 'INFO',
                },
            },
        })


    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)


   # 커스텀 진자 필터 등록
    from filters import format_datetime, format_datetime2
    app.jinja_env.filters['date_time'] = format_datetime
    app.jinja_env.filters['date_time2'] = format_datetime2

    from board.views import main_views, board_views, answer_views, auth_views
    from ml_model import ml_views
    app.register_blueprint(main_views.mbp)
    app.register_blueprint(board_views.cbp)
    app.register_blueprint(answer_views.abp)
    app.register_blueprint(auth_views.auth)
    app.register_blueprint(ml_views.mlbp)

    return app
