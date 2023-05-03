from flask import Blueprint, redirect, render_template, request, session, url_for
from alabar.data import get_topics_by_owner, get_topics_by_user, get_user_by_code, get_user_by_id
from alabar.models import Topic, Topic_ticket

alabar_bp = Blueprint('alabar', __name__)


#@alabar.route('/', methods=['POST'])
@alabar_bp.route('/alabar')
def index():
    #Se recuperan los topics de topic_ticket, topics que puede responder
    user = get_user_by_code(session['CURRENT_USER'])
    table_topics = get_topics_by_user(user.id_user)
    #Se recuperan los topics en los que es administrador de la tabla Topic
    # table_topics_owner = get_topics_by_owner(user_id)
    # for i in table_topics_owner:
    #     table_topics.append(i)
    for table_topic in table_topics:
        table_topic.id_owner = get_user_by_id(table_topic.id_owner).name_user
    return render_template('index.html', table_topics=table_topics)

@alabar_bp.route('/alabar/rating', methods=['GET', 'POST'])
def rating():
    "recuperar topic por id para comprobar el estado y recuperar topic ticket para comprobar si el user ha completado el topic"
    id_topic = request.form['topic_id']
    #topic = get_topic_by_id()
    topic = Topic()
    topic.title_topic = "Sprint 1"
    # status = 1 = active, status = 0 = inactive
    topic.status = 1

    #1 = completed, 0 = not completed
    topic_ticket = Topic_ticket()
    topic_ticket.completed = 0

    return render_template('rating.html', topic=topic, topic_ticket=topic_ticket)



@alabar_bp.route('/alabar/rating_results', methods=['POST'])
def rating_results():
    # save_answer()
    # update_ticket()
    return redirect(url_for('alabar.index'))

