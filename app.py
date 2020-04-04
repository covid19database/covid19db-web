from flask import Flask, request, redirect, url_for, render_template, jsonify
from utils import send_sms, random_code
app = Flask(__name__)


code_to_phone_number = {}  # TODO: move this to db, def don't leave this here


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        code = random_code()
        phone_number = request.form['phone_number']
        send_sms(
            phone_number=phone_number,
            message=f'Here is your super duper secret code: {code}')
        code_to_phone_number[code] = phone_number
        return redirect(url_for('code'))
    return render_template('login.html')


@app.route('/code', methods=('POST', 'GET'))
def code():
    if request.method == 'POST':
        code = request.form['code']
        if code not in code_to_phone_number:
            return jsonify({'success': False, 'message': 'nu'})

        phone_number = code_to_phone_number.pop(code)
        return jsonify({
            'success': True,
            'message': 'yey',
            'phone_number': phone_number
        })
    return render_template('code.html')


@app.route('/submit/')
def submit():
    return 'form here'


if __name__ == '__main__':
    app.run(debug=True)
