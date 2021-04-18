from flask import Flask, url_for, request, render_template

app = Flask(__name__)


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



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
