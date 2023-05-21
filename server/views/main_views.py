from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect

from server.models import Question

bp = Blueprint('main', __name__, url_prefix='/')


# bp는 Blueprint 클래스로 생성한 객체.
# Blueprint? 새로운 URL이 생길때마다 create_app 함수안에 추가하지 않아도 되게?
@bp.route('/')
def index():
    return redirect(url_for('question._list'))

@bp.route('/hello')
def hello_server():
    return render_template('index.html')

