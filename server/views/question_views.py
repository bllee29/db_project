from flask import Blueprint, render_template

from server.models import Question

# question_views.py 파일이 question 이름을 갖는 블루 프린트인것
bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/list')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html', question_list=question_list)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question)