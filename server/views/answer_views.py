from datetime import datetime
from flask import Blueprint, url_for, request, render_template, g, flash
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


@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:  # 에러처리
        flash('수정권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=answer.question_id))
    if request.method == "POST":  # post요청 - 수정한거 새로 저장하는거
        form = AnswerForm()
        if form.validate_on_submit():  # form이 유효하면
            form.populate_obj(answer)  # 불러온 answer을 수정한다.
            answer.modify_date = datetime.now()  # 수정일자 저장
            db.session.commit()  # 수정한 answer객체 저장
            return redirect(url_for('question.detail', question_id=answer.question_id))
    else:  # get요청 - 수정하기 할때는 form에 기존에 있던거 채워서 보여주고
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', form=form)


@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))
