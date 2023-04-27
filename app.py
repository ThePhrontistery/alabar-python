from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from alabar.data import get_topics_by_user
from alabar.models import init_app

app = Flask(__name__)

# The SECRET_KEY is used to encrypt session data in (persistent) cookies.
# >>> import secrets; secrets.token_hex(32)
app.config['SECRET_KEY'] = '642918690903c342d812d16cd33a4de4c8692483462550c9ddcd4303621cc1b2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alabar.db'
# app.config['EXPLAIN_TEMPLATE_LOADING'] = True
db = init_app(app)
#app.register_blueprint(crewverve_bp)
#app.register_blueprint(admin_bp)

app.app_context().push()
db.create_all()


@app.route('/')
def index():
    #return "Hola mundo"
    #return redirect(url_for('index'))
    #return render_template('index.html')

    user_id = 1


    table_topics = get_topics_by_user(user_id)
    return render_template('index.html', table_topics=table_topics)


if __name__ == '__main__':
    app.run(debug=True)
