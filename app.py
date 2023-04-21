from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/')
def index():
    return "Hola mundo"

if __name__ == '__main__':
    app.run(debug=True)
