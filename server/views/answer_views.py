from datetime import datetime
from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect

from server import db
from server.models import Question, Answer
from server.forms import AnswerForm

# answer_vies.py 파일이 answer이름을 갖는 블루 프린트인것
bp = Blueprint('answer', __name__, url_prefix='/answer')


# question_detail의 form의 method와 일치하게.
@bp.route('/create/<int:question_id>', methods=('POST',))
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now())
        question.answer_set.append(answer)
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_detail.html', question=question, form=form)