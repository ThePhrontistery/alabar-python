import datetime
from sqlalchemy import or_
from session_context import transactional_session
from .models import Topic_answer, User, Group, Topic, Topic_item, Topic_ticket, db
from sqlalchemy.sql import select



def get_topics_by_owner(user_id):
    #Select Topic by id_owner
    return db.session.execute(db.select(Topic).where(Topic.id_owner == user_id)).scalars().all()

def get_topic_by_id(id_topic):
    return db.session.execute(db.select(Topic).filter_by(id_topic=id_topic)).scalar_one_or_none()

def get_user_by_name(user_name):
    return db.session.execute(db.select(User).filter_by(name_user=user_name)).scalar_one_or_none()

def get_user_by_id(id_user):
    return db.session.execute(db.select(User).filter_by(id_user=id_user)).scalar_one_or_none()

def get_user_by_code(code_user):
    return db.session.execute(db.select(User).filter_by(code_user=code_user)).scalar_one_or_none()

def get_topics_ticket_by_user(user_id):
    "Select tabla Topic_ticket by user_id, para recuperar todos los objetos tickets de un usuario"
    return db.session.execute(db.select(Topic_ticket).where(Topic_ticket.user_id == user_id)).scalars().all()

def get_topic_ticket_by_topic(id_topic):
    "Select tabla Topic_ticket by id_topic, para recuperar todos tickets de un topic"
    return db.session.execute(db.select(Topic_ticket).where(Topic_ticket.topic_id == id_topic)).scalars().all()

def get_topic_ticket_by_topic_and_user(id_topic, id_user):
    "Select tabla Topic_ticket by id_topic, para recuperar todos los objetos tickets de un topic"
    return db.session.execute(db.select(Topic_ticket)
                              .where(Topic_ticket.topic_id == id_topic)
                              .where(Topic_ticket.user_id == id_user)).scalar_one_or_none()

def get_answer_by_id(id_topic):
    "Recuperamos todas las filas de la tabla topic_answer únicamente la columna answers para un id_topic"
    return db.session.execute(db.select(Topic_answer.answer).where(Topic_answer.id_topic==id_topic)).scalars().all()

def get_topics_by_user(user_id):
    "Get topic (must exist) associated users"
    topic_ticket = get_topics_ticket_by_user(user_id)
    topics_users = []
    for i in topic_ticket:
        topics_users.append(i.topics) 
    return topics_users

def get_topics_by_user_and_owner(user_id):

    h = select(Topic_ticket.topic_id).\
    where(Topic_ticket.user_id == user_id)

    s = select(Topic).\
    where(Topic.deleted_date == '9999-12-31 00:00:00.000000').\
    where(or_(Topic.id_owner == user_id,Topic.id_topic.in_(h)))

    return db.session.execute(s).scalars().all()

def save_results(id_topic,answer, user_code):
    "Estando en pantalla RESULT,al dar al botón SAVE se graba en BBDD"
    #try:
    with transactional_session() as session:
        #Metodo create_answer que inserta en 'Topic_answer' cada respuesta (devuelve answer) 
        create_answer(id_topic, answer)
        #Metodo update_ticket que actualiza en 'Topic_ticket' el campo completed:da por completado un ticket por topic y usuario
        update_ticket(user_code,id_topic)
        #Metodo update_topic que actualiza en 'Topic' el campo 'participation' y 'status'
        update_topic(get_topic_by_id(id_topic))
        result = True
        return result
    #except:
    #    db.session.rollback()
    #    return False

def create_answer(id_topic, answer):
    "Create record in topic_answer"
    #Creamos objeto answer de la clase Topic_answer pasando los campos por parametro para luego añadirlos a la tabla 
    answer = Topic_answer(id_topic=id_topic, answer=answer)
    return db.session.add(answer)

def update_ticket(user_code,id_topic):
    "Update record in topic_ticket: da por completado un ticket por topic y usuario"
    # Recupera un id_user para el user_name pasado por parametro
    user = get_user_by_code(user_code)
    # Search en topic_ticket de todos los ticket para el topic (id_topic) y el usuario (id_topic)
    ticket = get_topic_ticket_by_topic_and_user(id_topic, user.id_user)
    # Cambiamos el valor del campo 'completed'
    #1 = completed, 0 = not completed
    ticket.completed = not ticket.completed
    return db.session.execute(db.update(Topic_ticket).where(Topic_ticket.user_id == user.id_user)
                              .where(Topic_ticket.topic_id == id_topic)
                              .values(completed=ticket.completed))

def update_topic(topic):
    '''Update record in topic:
       Actualizamos en Topic la participacion y el status del topic (si es el ultimo usuario del grupo del topic en 
       contestar), pásandole el id_topic'''
    #answer tiene el resultado del metodo get_answers_by_id (que tiene todas las filas de la tabla topic_answer, 
    #únicamente la columna answers para un id_topic)
    answer = get_answer_by_id(topic.id_topic)

    #participation_total tiene el número de participantes que han respondido por cada id_topic: la longitud de answer 
    # me indica todas las personas que han respondido a ese id_topic
    participation_total = len(answer)

    #rating_total tiene el sumatorio de las ocurrencias de la 2 a la 16 de las filas recuperadas en get_answers_by_id
    #rating_total = sum(int(item_answer[e]) for item_answer in answer for e in range(2,17,2)) 

    #Recupero todos los tickets de un topic (mediante select tabla Topic_ticket by id_topic), la longitud me indica todos
    # los tickets de un id_topic
    topic_ticket = get_topic_ticket_by_topic(topic.id_topic)
    topic_ticket_total = len(topic_ticket)
    #rating es la media(total de rating entre el número de participantes)
    #survey.rating = rating_total / (participation_total*8)

    #participation es el número de usuario de projecto entre participantes
    topic.participation = participation_total*100 / topic_ticket_total
    # Status: True (Open - please vote), False (Closed - view results) 
    # Si la participacion es del 100, se cambia el status a closes (0)
    if topic.participation == 100:
        topic.status = False
    # Actualizamos status y participation
    return db.session.execute(db.update(Topic).where(Topic.id_topic == topic.id_topic)
                              .values(status=topic.status, participation= topic.participation))

def topic_reopen(id_topic):
    "Estando en pantalla RESULT,al dar al botón SAVE se graba en BBDD"
    #try:
    with transactional_session() as session:
    #Metodo update_topic que actualiza en 'Topic' el campo 'participation' y 'status'
       update_topic_reopen(get_topic_by_id(id_topic))
       result = True
       return result
    
def topic_delete(id_topic):
    "Estando en pantalla RESULT,al dar al botón SAVE se graba en BBDD"
    #try:
    with transactional_session() as session:
    #Metodo update_topic que actualiza en 'Topic' el campo 'participation' y 'status'
       update_topic_delete(get_topic_by_id(id_topic))
       result = True
       return result
    
def update_topic_reopen(topic):
    '''Update record in topic:
       Actualizamos en Topic el status del topic y la fecha de fin pásandole el id_topic'''
    topic.status = True
    topic.end_date = datetime.datetime(9999, 12, 31, 00, 00, 00, 00000)
    return db.session.execute(db.update(Topic).where(Topic.id_topic == topic.id_topic)
                              .values(status=topic.status, end_date= topic.end_date))

def update_topic_delete(topic):
    '''Update record in topic:
       Actualizamos en Topic la fecha de borrado pásandole el id_topic'''
    topic.deleted_date = datetime.date.today()
    return db.session.execute(db.update(Topic).where(Topic.id_topic == topic.id_topic)
                              .values(deleted_date= topic.deleted_date))