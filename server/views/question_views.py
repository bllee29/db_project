from datetime import datetime
from flask import Blueprint, render_template, url_for, request
from werkzeug.utils import redirect
from .. import db
from server.models import Question
from ..forms import QuestionForm, AnswerForm

# question_views.py 파일이 question 이름을 갖는 블루 프린트인것
bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/list')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html', question_list=question_list)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    form = QuestionForm() # form객체 생성후 return에 전달.
    # POST면 데이터 저장하고 메인페이지로
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data,
                            create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    # GET이면 질문요청 페이지로 간다.
    return render_template('question/question_form.html', form=form)
