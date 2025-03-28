
# Blueprint 기능을 사용
from flask import Blueprint, render_template, redirect, url_for, request
from ..models import Question, Answer
from ..forms import QuestionForm, AnswerForm
from app import db
from datetime import datetime


abp = Blueprint('answer', __name__, url_prefix='/answer')

# 댓글 조회

# 댓글 작성
# 1. GET - 작성 버튼을 누르면 작성 form으로 이동 
# 2. POST - 완료 버튼을 누르면 DB에 답변을 저장하고, 저장된 글을 확인케 위해 특정 글번호로 이동을합니다.
@abp.route('/create/', methods=('GET', 'POST'))
# @login_required # 실습 - answer_views에도 적용
def create():
    form = AnswerForm()
    if request.method == 'POST' and form.validate_on_submit():
        # db에 저장
        answer = Answer(question_id=2, content=form.content.data, create_date=datetime.now())
        db.session.add(answer)
        db.session.commit()
        # 2번글의 detail로 이동
        return redirect(url_for('board.detail', question_id=2))
    return render_template('answer/answerForm.html', form=form)


# 댓글 수정

# 댓글 삭제
