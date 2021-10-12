from flask import Flask, request, render_template, url_for

app = Flask(__name__)

menu = [{'name': 'Главная страница', 'url': '/'},
        {'name': 'Роллы', 'url': '/sushi'},
        {'name': 'Пиццы', 'url': '/pizza'},
        {'name': 'Салаты и закуски', 'url': '/salads'}
        ]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Магазин "Suchi Max"', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)
