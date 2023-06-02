from datetime import datetime
from flask import Blueprint, render_template, url_for, request, g, flash
from werkzeug.utils import redirect

# flash는 강제로 오류 발생시키는 함수, 로직에 오류가 발생하는 경우에 처리담당.

from .. import db
from server.models import Question
from ..forms import QuestionForm, AnswerForm
from server.views.auth_views import login_required


# question_views.py 파일이 question 이름을 갖는 블루 프린트인것
bp = Blueprint('question', __name__, url_prefix='/question')


# import한 Question 테이블의 entity들을 이용.
@bp.route('/list')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    # http://localhost:5000/question/list/?page=5 와 같이 마지막에 ?page=num 으로 인자를 전달해서 페이지를 보여준다.
    # num값이 비어있으면 1쪽을 보여줌
    # 원래 create_date순서로 정렬했는데 어짜피 생성일자 순으로 id부여받으니까 id순으로 해버리기?
    question_list = Question.query.order_by(Question.id.desc())
    question_list = question_list.paginate(page=page, per_page=20)  # 페이지
    # page는 현재 보여줄 page를 의미 per_page는 몇개씩 보여줄것인지.
    return render_template('question/question_list.html', question_list=question_list)  # 템플릿에 인자 전달.


# 해당하는 question_id에 따라 해당 entity의 내용을 표현
# 답변 달기에 사용할 form도 인자로 전달.
@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)  # 템플릿에 인자 전달.


# methods는 이 라우트에서 사용할 http method들을 선언?
@bp.route('/create', methods=('GET', 'POST'))
@login_required  # 함수 데코레이터
def create():
    form = QuestionForm() # form객체 생성후 return에 전달.
    # POST면 데이터 저장하고 메인페이지로
    if request.method == 'POST' and form.validate_on_submit():  # validate_~ 로 전송된 form 데이터의 정합성 확인.
        question = Question(subject=form.subject.data, content=form.content.data,
                            create_date=datetime.now(), user=g.user)  # 입력받은 내용을 기반으로 Question테이블에 새 entity생성
        db.session.add(question)
        db.session.commit()  # commint해야됨.
        return redirect(url_for('main.index'))
    # GET이면 질문요청 페이지로 간다.
    return render_template('question/question_form.html', form=form)  # 템플릿에 인자 전달. get을 언제 사용하는건지..
    # get은 question_list페이지에서 여기로 넘어올때 get요청한다, post는 이 라우트페이지에서 뭔가를 post할때 사용


@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정오류가 발생했습니다. 다시 시도해주세요.')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':  # POST 요청 - 수정하고 저장하기 버튼 누르면
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET 요청 - 수정하기 버튼 누르면
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)


@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))


@bp.route('/vote/<int:question_id>/')
@login_required
def vote(question_id):
    _question = Question.query.get_or_404(question_id)
    if g.user == _question.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))
