from flask import Blueprint, render_template, url_for, g
from werkzeug.utils import redirect


# main_views.py main.bp의 이름을 갖게 한다.
# main_views에서 사용하는 접두사는 '/'
# bp는 Blueprint 클래스로 생성한 객체.
# bp객체에 라우팅할 주소를 작성하여 server.__init__에 전부 작성을 하지않고 불러오는 방식으로.
bp = Blueprint('main', __name__, url_prefix='/')


# /으로 가면 table로 연결된다. table에서 바로 login_required로 로그인 요청
@bp.route('/')
def index():
    return redirect(url_for('table.main_page'))
# 이름..을 전달하면 알아서 검색을 하는듯.
# question_views의 _list로 redirect 해주는듯. url_for하면 그 blueprint도 검색을 하는듯


@bp.route('/table')
def table():
    return render_template('timetable.html')


@bp.route('/hello')
def hello_server():
    return render_template('index.html')

