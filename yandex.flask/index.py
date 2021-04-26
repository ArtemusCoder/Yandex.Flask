from flask import Flask, request, render_template, redirect, make_response, jsonify
from werkzeug.exceptions import abort

from forms.loginform import LoginForm
import os

from data import db_session, jobs_api
from data.users import User
from data.jobs import Jobs
from data.departments import Department

from forms.user import RegisterForm
from forms.depart import DepartForm
from forms.job import JobAdd
from flask_restful import reqparse, abort, Api, Resource

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import users_resource
import jobs_resource

app = Flask(__name__)
api = Api(app)
api.add_resource(users_resource.UsersListResource, '/api/v2/users')
api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:job_id>')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    db_session.global_init("db/database.db")
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    return render_template("index.html", jobs=jobs)


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def addjob():
    db_session.global_init("db/database.db")
    db_sess = db_session.create_session()
    form = JobAdd()
    if form.validate_on_submit():
        job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        current_user.job.append(job)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('job_add.html', title='Добавление работы', form=form)


@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    db_session.global_init("db/database.db")
    form = JobAdd()
    if request.method == "GET":
        db_sess = db_session.create_session()
        if current_user.id == 1:
            job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        else:
            job = db_sess.query(Jobs).filter(Jobs.id == id,
                                             Jobs.user == current_user
                                             ).first()
        if job:
            form.team_leader.data = job.team_leader
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id == 1:
            job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        else:
            job = db_sess.query(Jobs).filter(Jobs.id == id,
                                             Jobs.user == current_user
                                             ).first()
        print(job)
        if job:
            job.team_leader = form.team_leader.data
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('job_add.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    if current_user.id == 1:
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    else:
        job = db_sess.query(Jobs).filter(Jobs.id == id,
                                         Jobs.user == current_user
                                         ).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/training/<prof>')
def training(prof):
    if 'инженер' in prof or 'строитель' in prof:
        return render_template('training1.html', title='Инженерные тренажеры')
    else:
        return render_template('training2.html', title='Научные симуляторы')


@app.route('/list_prof/<list>')
def list_prof(list):
    if list == 'ul':
        return render_template('list.html', title='Список профессий', design=False)
    elif list == 'ol':
        return render_template('list.html', title='Список профессий', design=True)


@app.route('/answer')
@app.route('/auto_answer')
def auto_answer():
    param = {}
    param['title'] = 'Анкета'
    param['surname'] = 'Иванов'
    param['name'] = 'Артемий'
    param['education'] = 'среднее'
    param['profession'] = 'киберинженер'
    param['sex'] = 'male'
    param['motivation'] = 'посмотрел фильм Марсианин, захотел побывать там'
    param['ready'] = True
    return render_template('auto_answer.html', **param)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/distribution')
def distribution():
    param = {}
    param['title'] = 'Размещение по каютам'
    param['members'] = ['Ридли Скот', 'Энди Уир', 'Марк Уотни', 'Венката Капур', 'Тедди Сандерс',
                        'Шон Бин']
    return render_template('distribution.html', **param)


@app.route('/table/<sex>/<int:age>')
def table(sex, age):
    param = {}
    param['title'] = 'Оформление каюты'
    param['sex'] = sex
    param['age'] = int(age)
    return render_template('table.html', **param)


@app.route('/gallery', methods=['GET', 'POST'])
@app.route('/galery', methods=['GET', 'POST'])
def gallery():
    if request.method == 'GET':
        files = os.listdir('static/img/gallery')
        print(files)
        param = {}
        param['title'] = 'Пейзажи Марса'
        param['files'] = files
        return render_template('gallery.html', **param)
    elif request.method == 'POST':
        files = os.listdir('static/img/gallery')
        f = request.files['file']
        f.save(f'static/img/gallery/{len(files) + 1}.jpg')
        return "Форма отправлена"


@app.route('/member')
def member():
    pass


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    db_session.global_init("db/database.db")
    db_sess = db_session.create_session()
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,

        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/departments')
def departments():
    db_session.global_init("db/database.db")
    db_sess = db_session.create_session()
    depart = db_sess.query(Department)
    return render_template("departments.html", jobs=depart)


@app.route('/add_depart', methods=['GET', 'POST'])
@login_required
def add_depart():
    db_session.global_init("db/database.db")
    db_sess = db_session.create_session()
    form = DepartForm()
    if form.validate_on_submit():
        depart = Department(
            title=form.title.data,
            chief=form.title.data,
            members=form.members.data,
            email=form.email.data
        )
        current_user.department.append(depart)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/departments')
    return render_template('departform.html', title='Добавление работы', form=form)


@app.route('/depart/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_depart(id):
    db_session.global_init("db/database.db")
    form = DepartForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        if current_user.id == 1:
            depart = db_sess.query(Department).filter(Department.id == id).first()
        else:
            depart = db_sess.query(Department).filter(Department.id == id,
                                                      Department.user == current_user
                                                      ).first()
        if depart:
            form.title.data = depart.title
            form.chief.data = depart.chief
            form.members.data = depart.members
            form.email.data = depart.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id == 1:
            depart = db_sess.query(Department).filter(Department.id == id).first()
        else:
            depart = db_sess.query(Department).filter(Department.id == id,
                                                      Department.user == current_user
                                                      ).first()
        if depart:
            depart.title = form.title.data
            depart.chief = form.chief.data
            depart.members = form.members.data
            depart.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('departform.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/depart_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def depars_delete(id):
    db_sess = db_session.create_session()
    if current_user.id == 1:
        depart = db_sess.query(Department).filter(Department.id == id).first()
    else:
        depart = db_sess.query(Department).filter(Department.id == id,
                                                  Department.user == current_user
                                                  ).first()
    if depart:
        db_sess.delete(depart)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    db_session.global_init("db/database.db")
    app.register_blueprint(jobs_api.blueprint)
    app.run(port=8080, host='127.0.0.1')
