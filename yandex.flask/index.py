from flask import Flask, url_for, request, render_template, redirect
from loginform import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Заготовка')


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
        return redirect('/success')
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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
