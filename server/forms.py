from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

# wtforms는 양식만들기 유효성검사 및 CSRF보호를 포함한 다양한 기능을 제공하는 라이브러리
# FlaskForm을 통해서 양식을 만들 수 있다.


# validators로 뭐 기능 추가하는듯 DataRequired로 필수입력하게 제한할 수 있다.

class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])
    course = StringField('수업', validators=[DataRequired()])


class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])


class UserCreateForm(FlaskForm):
    jobs = StringField('사용자구분')
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])


class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])


class CourseCreateForm(FlaskForm):
    coursename = StringField('수업이름', validators=[DataRequired()])
    cdate1 = StringField('수업요일1', validators=[DataRequired()])
    startTime1 = StringField('수업시작시간', validators=[DataRequired()])
    classTime1 = StringField('몇시간 수업', validators=[DataRequired()])
    cdate2 = StringField('수업요일2')
    startTime2 = StringField('수업시작시간')
    classTime2 = StringField('몇시간 수업')


class CourseEnrollForm(FlaskForm):
    coursename = StringField('수업이름', validators=[DataRequired()])
