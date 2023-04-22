from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('about.html')


@app.route('/info')
def info():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
