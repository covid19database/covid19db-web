from flask import Flask, request, redirect, url_for, render_template, jsonify
from utils import send_sms
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        send_sms(request.form['phone_number'], 'Here is your super duper secret code: HUEHUE')
        return redirect(url_for('code'))
    return render_template('index.html')


@app.route('/code', methods=('POST', 'GET'))
def code():
    if request.method == 'POST':
        return jsonify({
            'Das': 'right' if request.form['code'] == 'HUEHUE' else 'wrong'
        })
    return render_template('code.html')


@app.route('/submit/')
def submit():
    return 'form here'


if __name__ == '__main__':
    app.run(debug=True)
