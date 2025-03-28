from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired("10글자 넘는 글자를 입력하세요!!"),  Length(max=10)])
    content = TextAreaField('내용', validators=[DataRequired("내용을 꼭 입력하셔야 합니다!!!")])

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired()])
