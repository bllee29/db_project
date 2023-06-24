from server import db


# many to many 관계 설정. N:N
# N:N관계를 표현하는 테이블

# 질문 답변 관계
question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)

answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)

# 사용할 Table들


# 수업-학생관계
class CourseStudent(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    course_id = db.Column(db.String(100), db.ForeignKey('course.id', ondelete='CASCADE'), primary_key=True)
    # user = db.relationship('User', backref=db.backref('course_set'))


# 수업 table
class Course(db.Model):
    id = db.Column(db.String(100), nullable=False, primary_key=True)  # 수업이름
    cDate1 = db.Column(db.String(10), nullable=False)  # 수업요일1
    startTime1 = db.Column(db.Float(), nullable=False)  # 시작시간
    classTime1 = db.Column(db.Float(), nullable=False)  # 몇시간 하는지
    cDate2 = db.Column(db.String(10), nullable=True)  # 수업요일2
    startTime2 = db.Column(db.Float(), nullable=True)  # 시작시간
    classTime2 = db.Column(db.Float(), nullable=True)  # 몇시간 하는지
    # 교수 : 수업 = 1 : n 관계
    professor = db.Column(db.String(20), db.ForeignKey('user.username', ondelete='CASCADE'), nullable=False)
    pf = db.relationship('User', backref=db.backref('professor'))


# question table
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 자동으로 부여되는 글번호
    subject = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))  # 글쓴이 정보
    modify_date = db.Column(db.DateTime(), nullable=True)
    # N:N관계는 secondary로 추가. 데이터는 question_voter에 저장. question모델에서 참조가능.
    # backref에 같은이름 사용 불가.
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))
    # 수업과 1:N 관계 질문 n개는 수업 1개에 속해있다.
    course_id = db.Column(db.String(100), db.ForeignKey('course.id', ondelete='CASCADE'), nullable=False)
    course = db.relationship('Course', backref=db.backref('course'))


# answer table
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 자동으로 부여되는 글번호
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    # backref = 역참조 question.answer_set으로 그 question에 대한 answer들에 접근가능
    # 뭘 기반으로 접근하는지? question.id로 지정된 foreignkey
    # answer_set의 이름으로 question에서 해당 question에 1대다관계로 매핑된 answer들에 접근 할 수 있다.
    # 테이블의 내용에는 포함되지 않는다.
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))  # 질문에 달린 답변들
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))


# user table
class User(db.Model):
    jobs = db.Column(db.String(10), nullable=False)  # 학생 교수 구분
    id = db.Column(db.Integer, primary_key=True)    # id
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


