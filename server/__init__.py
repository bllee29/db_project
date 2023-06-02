from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from server import config

# __init__.py 디렉토리가 패키지로 인식되게 하는역할 / 패키지를 초기화 하는 역할
# 3.3버전부터는 없어도 패키지로 인식하는듯?

# SQLAlchemy에서 db설정
db = SQLAlchemy()
migrate = Migrate()


# 애플리케이션 팩토리
# app객체를 생성하는 함수.
# app 객체를 전역으로 사용할 때 발생하는 문제를 예방.
# create_app()함수를 인식하는 것 같다. create_app함수의 이름을 바꾸니 flask run 명령어로 실행이 되지 않음.
# create_app() 또는 그냥 실행해서 app 객체를 생성하면 flask run이 되는듯.
def create_app():
    app = Flask(__name__)  # __name__ 현재 모듈의 이름 아마 server이 전달될듯. 그 내부의 파일들, 템플릿들을 찾는데 사용하는듯
    app.config.from_object(config)  # import한 config 파일 받아온다.

    # database / ORM
    db.init_app(app)  # sqlAlchemy로 불러온 db에 현재 app객체를 연결 ORM?
    migrate.init_app(app, db)  # migrate도 설정.
    from server import models  # 이건 어디서 사용하는지 모르겠네 아마 migrate객체가 참조하는 것 같은데 flask db migrate명령어에서 사용하는듯

    # 블루프린트
    # main_views 블루프린트객체 등록
    # main함수에서 라우팅안하고 bp에서 하는듯
    # app에 내가 생성한 blueprint들을 등록해서 라우팅.
    from server.views import main_views, question_views, answer_views, auth_views  # bp들을 import하고 연결
    app.register_blueprint(main_views.bp)  # import한 main_views의 bp객체
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    #필터
    # 템플릿 필터 -- 템플릿 엔진에서 사용되는 필터로 주어진 데이터를 가공하거나 포맷팅한다.
    # 함수를 임포트해서 app에 datetime이라는 이름으로 필터를 등록했다.
    from server.filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app
