from flask import Flask, request, redirect, url_for, jsonify, \
    render_template as flask_render_template
from flask_login import LoginManager, login_user, UserMixin, login_required, \
    current_user, logout_user
from utils import send_sms, random_code
import requests
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

login_manager = LoginManager()
login_manager.init_app(app)

API_BASE_URL = os.environ['API_BASE_URL']
code_to_phone_number = {}  # TODO: move this to db, def don't leave this here


def render_template(*args, **kwargs):
    kwargs['random_code'] = random_code()
    kwargs['today'] = datetime.datetime.today().strftime('%Y-%m-%d')
    kwargs['now'] = datetime.datetime.now().strftime('%H:%M')
    return flask_render_template(*args, **kwargs)


class User(UserMixin):

    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
@login_required
def home():
    traces = requests.get(os.path.join(API_BASE_URL, 'traces/'))
    return render_template('home.html', traces=traces.json())


@app.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated and request.args.get('force') != "true":
        return redirect(url_for('home'))
    if request.method == 'POST':
        code = random_code()
        phone_number = request.form['phone_number']
        send_sms(
            phone_number=phone_number,
            message=f'Here is your super duper secret code: {code}')
        code_to_phone_number[code] = phone_number
        return redirect(url_for('code', phone_number=phone_number))
    return render_template('auth.html', action=url_for('login'), name='phone_number')


@app.route('/code', methods=('POST', 'GET'))
def code():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        code = request.form['code']
        if code not in code_to_phone_number:
            return jsonify({'success': False, 'message': 'nu'})

        phone_number = code_to_phone_number.pop(code)
        login_user(User(phone_number))
        return redirect(url_for('home'))
    return render_template('auth.html',
        h2='Type in your security code.',
        p=f"We sent a code to your phone: <b>{request.args.get('phone_number')}</b>",
        action=url_for('code'),
        name='code',
        placeholder='Code')


@app.route('/check/', methods=('POST', 'GET'))
def check():
    if request.method == 'POST':
        data = {
            'id': -1,
            'plus_codes': request.form['place']
        }
        response = requests.post(os.path.join(API_BASE_URL, 'traces/'), json=data)
        return render_template('result.html')
    return redirect(url_for('index'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
