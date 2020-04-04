from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Submit at /submit/'

@app.route('/submit/')
def submit():
    return 'form here'
