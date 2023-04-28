from flask import Blueprint, redirect, render_template, request, session, url_for

from alabar.data import get_topics_by_user


from .data import get_topics_by_user

alabar_bp = Blueprint('alabar', __name__)


#@alabar.route('/', methods=['POST'])
@alabar_bp.route('/alabar')
def index():
    #pending_surveys = get_pending_surveys_by_user(session['CURRENT_USER'])
    user_id = 1
    table_topics = get_topics_by_user(user_id)
    return render_template('index.html', table_topics=table_topics)


