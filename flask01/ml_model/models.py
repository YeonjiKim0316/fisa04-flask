from app import db
from datetime import datetime

# db.Model을 상속받은 테이블을 만듭니다.
class Insurance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    children = db.Column(db.Integer, nullable=False)
    smoker = db.Column(db.Boolean, nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    sex = db.Column(db.String(10), nullable=False)
    region = db.Column(db.String(10), nullable=False)
    expected_insurance_fee = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    # user테이블 pk로 작성자를 구분 - nullable=False 로 변경, ondelete='CASCADE'로 변경 
    user = db.relationship('User', backref=db.backref('inference_set'))