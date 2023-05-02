from flask import Blueprint, redirect, render_template, request, session, url_for

from alabar.data import get_topics_by_user, get_user_by_id

alabar_bp = Blueprint('alabar', __name__)


#@alabar.route('/', methods=['POST'])
@alabar_bp.route('/alabar')
def index():
    #pending_surveys = get_pending_surveys_by_user(session['CURRENT_USER'])
    user_id = 1
    table_topics = get_topics_by_user(user_id)
    for table_topic in table_topics:
        table_topic.id_owner = get_user_by_id(table_topic.id_owner).name_user
    return render_template('index.html', table_topics=table_topics)


