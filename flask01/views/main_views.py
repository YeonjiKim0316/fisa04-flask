from flask import Blueprint

# 특정 /main/ 하위에 있는 함수들을 일괄적으로 관리하기 위한 flask의 기능
                # 코드에서 부르는 상대적 이름, 실제 파일명, url에 매칭되는 경로 
mbp = Blueprint('main', __name__, url_prefix='/main')

# localhost:5001/main/
@mbp.route('/')
def hello(username):
    return f'{__name__} hello'

# Flask에서 값을 주소줄로 입력받아서 사용하는 방법
