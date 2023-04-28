from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from alabar.data import get_topics_by_user, get_user_by_name
from alabar.middleware import authenticate_handler
from alabar.models import init_app
from alabar.views import alabar_bp

app = Flask(__name__)

# The SECRET_KEY is used to encrypt session data in (persistent) cookies.
# >>> import secrets; secrets.token_hex(32)
app.config['SECRET_KEY'] = '642918690903c342d812d16cd33a4de4c8692483462550c9ddcd4303621cc1b2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alabar.db'
# app.config['EXPLAIN_TEMPLATE_LOADING'] = True
db = init_app(app)
app.register_blueprint(alabar_bp)
#app.register_blueprint(admin_bp)

app.app_context().push()
db.create_all()

@app.before_request
def before_request():
    return authenticate_handler(None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_name(username)

        if user is None or not user.check_password(password):
            error = 'Invalid username or password'
        else:
            # Note: Flask session. NOT SqlAlchemy...
            session['CURRENT_USER'] = username
            return redirect(url_for('alabar.index'))
 
    return render_template('login.html', error=error)

@app.route('/logout', methods=['GET'])
def logout():

    # Note: Flask session. NOT SqlAlchemy...
    del session['CURRENT_USER']
    return redirect(url_for('login'))

@app.route('/')
def index():
    #return "Hola mundo"
    #return redirect(url_for('index'))
    #return render_template('index.html')

    #user_id = 1


    #table_topics = get_topics_by_user(user_id)
    #return render_template('index.html', table_topics=table_topics)
    return redirect(url_for('alabar.index'))

@app.route('/page-not-found')
def page_not_found():
    return render_template('error.html', error_message="Page not found", error_description="This isn't the page you are looking for....")

if __name__ == '__main__':
    app.run(debug=True)
