
# Blueprint 기능을 사용
from flask import Blueprint, render_template, redirect, url_for, request, g, flash
from ..models import Question, Answer
from ..forms import QuestionForm, AnswerForm
from app import db
from datetime import datetime
from board.views.auth_views import login_required

abp = Blueprint('answer', __name__, url_prefix='/answer')

# 댓글 작성
# 1. GET - 작성 버튼을 누르면 작성 form으로 이동 
# 2. POST - 완료 버튼을 누르면 DB에 답변을 저장하고, 저장된 글을 확인케 위해 특정 글번호로 이동을합니다.
@abp.route('/create/<int:question_id>', methods=['POST'])
@login_required # 실습 - answer_views에도 적용
def create(question_id):
    form = AnswerForm()
    question = Question.query.get(question_id)
    if form.validate_on_submit(): # csrf_token + 로그인기능
        # db에 저장
        answer = Answer(question_id=question_id, content=form.content.data, 
                        create_date=datetime.now(), user=g.user)
        db.session.add(answer)
        db.session.commit()
        # 2번글의 detail로 이동
        return redirect(url_for('board.detail', question_id=question_id))
    return render_template('board/boardDetail.html', question=question, form=form)



# 개별 게시글을 수정
# 로그인 여부 확인
@abp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    # db에서 글을 가져온다
    answer = Answer.query.get_or_404(answer_id)
    # 댓글이 포함된 글번호도 가져옵니다.
    question_id = answer.question_id
    # 현재 작성자와 로그인한 사람이 같은 사람이지 확인
    if answer.user != g.user:
        # 아니면 '권한이 없습니다' 에러 flash
        flash('수정 권한이 없습니다.')
        # 글의 본문으로 돌려보냅니다.
        return redirect(url_for('board.detail', question_id=question_id))

    # 글의 작성자와 로그인한 사람이 같으면(권한 O), POST인지 확인하고
    if request.method == 'POST':
       # QuestionForm에 값을 미리 가져온 다음에 
        form = AnswerForm()
        if form.validate_on_submit():
        # 변경한 값을 db에 다시 반영
            form.populate_obj(answer) # 화면에 원래 db에서 가져온 값을 form에 넣어서 보여줍니다.
            db.session.commit()
            # 수정된 글의 본문으로 돌려보냅니다.
            return redirect(url_for('board.detail', question_id=question_id))
    else: # GET으로 왔을 때
        # 수정화면으로 FORM과 돌려보냅니다.
        form = AnswerForm(obj=answer) 
    return render_template('answer/answerForm.html', form=form, answer_id=answer_id, modify=True)

@abp.route("/delete/<int:answer_id>")
@login_required
def delete(answer_id):
    # 글을 가져옴
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question_id
    # 현재 접속한 사용자와 글의 작성자가 일치하는지 확인
    if g.user != answer.user: 
        flash('삭제권한이 없습니다')
    #     일치하지 않으면 -> 삭제권한이 없습니다 메시지 출력
        return redirect(url_for('board.detail', question_id=question_id))
    #     원래 글로 되돌아감
    db.session.delete(answer)
    db.session.commit()
    # 댓글이 삭제된 게시글 상세 페이지로 되돌아감 
    return redirect(url_for('board.detail', question_id=question_id))
