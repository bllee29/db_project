from datetime import datetime
from flask import Blueprint, url_for, request, render_template, g
from werkzeug.utils import redirect

from server import db
from server.models import Question, Answer
from server.forms import AnswerForm  # WTForms를 사용한 form형식 class네
from server.views.auth_views import login_required

# answer_vies.py 을 answer의 이름을 갖게한다. 여기 있는 페이지들의 접두사는 /answer
bp = Blueprint('answer', __name__, url_prefix='/answer')


# question_detail의 <form> method와 일치하게.
@bp.route('/create/<int:question_id>', methods=('POST',))
@login_required  # 함수 데코레이터
def create(question_id):
    form = AnswerForm()  # 질문 밑에 표시할 답변등록 창.
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():  # post밖에 없으니까 method는 검사 안함.
        content = request.form['content']  # 입력받은 content를 가져온다.
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)  # 새 answer entity 생성
        question.answer_set.append(answer)
        db.session.commit()  # commit해야됨.
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_detail.html', question=question, form=form)