
# Blueprint 기능을 사용
from flask import Blueprint, render_template, redirect, url_for, request
from ..models import Question
from ..forms import QuestionForm
from app import db
from datetime import datetime


cbp = Blueprint('board', __name__, url_prefix='/board')


# templates 디렉토리 안에 들어있는 file 경로를 읽고, view에 작성한 객체를 달아서 렌더링해서 전달
# 전체 게시글을 db에서 조회해서 가져와서 리스트
@cbp.route('/list')
def list():
    question = Question.query.all()
    return render_template('board/boardList.html', question_list=question)

# 개별 게시글을 조회할 수 있는 함수
@cbp.route('/details/<int:question_id>/')
def detail(question_id):
    # get_or_404() 메서드로 값을 조회하면 404에러를 발생시킵니다.
    # question = Question.query.get(question_id)
    question = Question.query.get_or_404(question_id)
    return render_template('board/boardDetail.html', question=question)

# 개별 게시글을 작성
# 1. 작성 버튼을 누르면 게시글 작성하기 위한 form으로 이동 
# 2. 완료 버튼을 누르면 DB에 글을 저장하고, 저장된 글을 확인케 위해 전체 list로 이동을합니다.
@cbp.route('/create/', methods=('GET', 'POST'))
# @login_required # 실습 - answer_views에도 적용
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('board.list'))
    return render_template('board/questionForm.html', form=form)

# 개별 게시글을 삭제

# 개별 게시글을 수정

# 댓글 작성

# 댓글 수정

# 댓글 삭제


# Blueprint 기능을 사용해서 collection/no1/
@cbp.route('/no1')
def hello2():
    return f'{__name__} 첫번째'
    
@cbp.route('/no2')
def hello3():
    return f'{__name__} 두번째'
    