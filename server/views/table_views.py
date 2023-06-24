from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.utils import redirect
from sqlalchemy import exc

from server.forms import CourseCreateForm, CourseEnrollForm
from .. import db
from server.models import User, Course, CourseStudent
from server.views.auth_views import login_required

bp = Blueprint('table', __name__, url_prefix='/table')


@bp.route('/page')
@login_required
def main_page():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)
    # 쿼리 결과 전부 가져옴
    courseset = db.session.query(CourseStudent).filter_by(user_id=user_id)
    courselist = list()
    # user가 듣는 수업가져옴
    for course in courseset:
        a = str(course).split(' ')[2][:-1]
        courselist.append(a)

    return render_template('/table/timetable.html', user=user, cl=courselist)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    form = CourseCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        course1 = Course.query.filter_by(id=form.coursename.data).first()
        if not course1:
            course = Course(id=form.coursename.data,
                            professor=g.user.username,
                            cDate1=form.cdate1.data,
                            startTime1=form.startTime1.data,
                            classTime1=form.classTime1.data,
                            cDate2=form.cdate2.data,
                            startTime2=form.startTime2.data,
                            classTime2=form.classTime2.data
                            )
            db.session.add(course)
            db.session.commit()
            return redirect(url_for('main.index'))

        else:
            flash('이미 존재하는 강의입니다.')
            flash(course1)
    return render_template('table/create.html', form=form)


@bp.route('/enroll', methods=('GET', 'POST'))
@login_required
def enroll():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)
    form = CourseEnrollForm()

    course1 = db.session.query(CourseStudent).\
        filter(CourseStudent.user_id == user_id, CourseStudent == form.coursename.data).first()

    if request.method == 'POST' and form.validate_on_submit():

        if not course1:
            course = CourseStudent(user_id=g.user.id,
                                   course_id=form.coursename.data
                                   )
            try:
                db.session.add(course)
                db.session.commit()
            except exc.IntegrityError:
                flash('이미 등록된 강의거나 존재하지 않는 강의입니다.')
                return redirect(url_for('table.enroll'))

            return redirect(url_for('main.index'))
        else:
            flash('이미 등록된 강의거나 존재하지 않는 강의입니다.')
    return render_template('/table/enroll.html', user=user, form=form)
