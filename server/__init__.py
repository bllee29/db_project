from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from server import config


db = SQLAlchemy()
migrate = Migrate()


# 애플리케이션 팩토리
# app 객체를 전역으로 사용할 때 발생하는 문제를 예방.
def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # database
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # main_views 블루프린트객체 등록
    # main함수에서 라우팅안하고 bp에서 하는듯
    from server.views import main_views, question_views, answer_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)

    return app


#
#     @app.route('/')
#     def index():
#         return render_template('index.html')
#
#     @app.route('/register')
#     def register():
#         return render_template('register.html')
#
#     @app.route('/post')
#     def board():
#         return render_template('post.html')
#
#     @app.route('/post/second')
#     def second():
#         return render_template('posts/second.html')
#
#     @app.route('/post/first')
#     def posts():
#         return render_template('posts/first.html')
#
#     if __name__ == '__main__':
#         app.run(debug=True)
