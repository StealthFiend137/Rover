import os
from flask import Flask, render_template, send_from_directory


app = Flask(__name__, static_folder='static', template_folder='static')

@app.route('/')
def hello_world():
    return "hello world"

@app.route('/control')
def serve_static():
    return render_template("BrowserController.html")

if __name__ == '__main__':
    app.run(debug=True)