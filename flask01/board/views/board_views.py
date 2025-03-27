
# Blueprint 기능을 사용해서 collection/no2/
from flask import Blueprint
from ..models import Question

cbp = Blueprint('collection', __name__, url_prefix='/board')

# Blueprint 기능을 사용해서 collection/no1/
@cbp.route('/no1')
def hello2():
    return f'{__name__} 첫번째'
    
@cbp.route('/no2')
def hello3():
    return f'{__name__} 두번째'
    