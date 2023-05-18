import datetime
import numpy as np
from sqlalchemy import func, or_
from session_context import transactional_session
from .models import Answer, Stat, Topic_answer, Topic_data, Topic_item, User, Topic, Topic_ticket, db
from sqlalchemy.sql import select

typetopics = [
    "MultipleChoiceTextTopic",
    "MultipleChoiceImageTopic",
    "SingleChoiceTextTopic",
    "SingleChoiceImageTopic",
    "♠A of ♠Topic",
    "RatingTopic"
]

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

def get_topic_answers_by_topic_id(id_topic):
    return db.session.execute(select(Topic_answer).where(Topic_answer.id_topic == id_topic)).scalars().all()

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
    "Estando en pantalla de lista, pulsar el boton reopen"
    with transactional_session() as session:
       update_topic_reopen(get_topic_by_id(id_topic))
       result = True
       return result
    
def topic_delete(id_topic):
    "Estando en pantalla de lista, pulsar el boton delete"
    with transactional_session() as session:
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

def show_result(id_topic):
    # Recuperamos lista de respuestas posibles:
    possible_answers = get_possible_answers()
    # recuperamos lista de respuestas dadas para un topic determinado de dos maneras:
    #1: recuperamos toda la fila de la tabla topic answers y nos quedamos con el campo answer
    # voted_answers_class = get_topic_answers_by_topic_id(id_topic)
    # voted_answers = [int(answer.answer) for answer in voted_answers_class]
    #2: recuperamos solo el campo answer directamente en la query:
    voted_answers = [int(i) for i in get_answer_by_id(id_topic)]

    #las posibles respuestas estan inicializadas con contador 0, contamos cuantas respuestas hay de cada posible respuesta:
    possible_answers = update_answers_count(voted_answers, possible_answers)

    #Recuperamos la respuesta media:
    # ESTO ES MUY FEO? HAY UNA MEJOR MANERA DE HACERLO?
    #possible_answers = [answer_text for answer_text in answers_text if average == answer_text.order][0]
    # por defecto se muestra la primera respuesta posible (very sad):
    average_answer = 0
    average = 0
    if voted_answers:
        average = round(get_average(voted_answers))
    #dentro de las posibles respuestas, buscamos cual de ellas corresponde a la media
    for i in (answer for answer in possible_answers if average == answer.order):
        average_answer = i
        
    results = Stat(possible_answers, average_answer)
    return results

def get_possible_answers():
    a = Answer("😭", 1, "Sad", 0)
    b = Answer("🙁", 2, "Dissapointed", 0)
    c = Answer("😐", 3, "Neutral", 0)
    d = Answer("😊", 4, "Contented", 0)
    e = Answer("😃", 5, "Happy", 0)
    answers = [a, b, c, d, e]
    return answers

def get_average(voted_answers):
    answers_count = len(voted_answers)
    unique_answers_list = get_unique_answers(voted_answers)
    answers_sum = 0
    for voted_answer in unique_answers_list:
        voted_answer_count = sum(map(lambda i: i == voted_answer, voted_answers))
        answers_sum = answers_sum + voted_answer * voted_answer_count
    average = answers_sum/answers_count
    return average

def get_unique_answers(voted_answers):
    x = np.array(voted_answers)
    return np.unique(x).tolist()

def update_answers_count(voted_answers, possible_answers):
    "Actualización count"
    #para poder utilizar el sum necesitamos pasar de tipo lista a array
    x = np.array(voted_answers)
    for answer in possible_answers:
        answer.count = (x == answer.order).sum()
    return possible_answers

def save_topic_results(topic_data):
    "Estando en pantalla NEW TOPIC,al dar al botón SAVE se graba en BBDD"
    with transactional_session() as session:
        #Metodo create_topic que inserta en 'Topic' cada topic (devuelve topic) pasando topic con los parametros
        topic_select = create_topic(topic_data)
        #Metodo create_topic_item que inserta en 'Topic_item' 
        #create_topic_item(???)
        result = True
        return topic_select
        #return last_id

def create_topic(topic_data):
    "Create record in topic"
    #Creamos objeto topic de la clase Topic  pasando los campos por parametro para luego añadirlos a la tabla 
    topic_new = Topic(title_topic=topic_data.title_topic, id_owner=topic_data.id_owner,type_topic=topic_data.type_topic,
                  start_date=datetime.datetime.now(),end_date=topic_data.end_date,status=True,participation=0,
                  deleted_date=datetime.datetime(9999, 12, 31))
    db.session.add(topic_new)
         
    return Topic_data(title_topic=topic_data.title_topic,id_owner=topic_data.id_owner,type_topic=topic_data.type_topic,
                       end_date=topic_data.end_date)

def get_id_topic_by_data(topic_select):
    "Select tabla Topic by data (campos de pantalla), para recuperar el topic creado (campo id_topic)"
    return db.session.execute(db.select(Topic)
                              .where(Topic.title_topic == topic_select.title_topic)
                              .where(Topic.id_owner == topic_select.id_owner)
                              .where(Topic.type_topic == topic_select.type_topic)
                              .where(Topic.end_date == topic_select.end_date)).scalar_one_or_none()
                                                            

def get_max_id_order_in_topic_item(id_topic):
    "Select tabla Topic_item by id_topic, para recuperar el id order maximo para cada id_topic"
    #return db.session.execute(db.select([db.func.max(Topic_item.id_order)])
    #  .where(Topic_item.id_topic == id_topic)).scalar()
    return db.session.query(func.max(Topic_item.id_order)
           .filter(Topic_item.id_topic == id_topic)).scalar()

def save_results_item(id_topic, id_order,text_answers):
    "Estando en pantalla NEW TOPIC,al dar al botón SAVE se graba en BBDD"
    with transactional_session() as session:
        #Metodo create_topic_item que inserta en 'Topic_item' cada item (devuelve item) 
        create_topic_item(id_topic, id_order,text_answers)
        result = True
        return result
    
def create_topic_item(id_topic, id_order,text_answers):
    "Create record in topic_item"
    #Creamos objeto topic_item de la clase Topic_item pasando los campos por parametro para luego añadirlos a la tabla 
    item = Topic_item(id_topic=id_topic, id_order=id_order,text_answers=text_answers)
    return db.session.add(item)                      
                              

def get_topic_item_by_id_topic(id_topic):
    "Select tabla Topic_item by id_topic, para recuperar todos los topic_item"
    return db.session.execute(db.select(Topic_item)
                              .where(Topic_item.id_topic == id_topic)).scalars().all()
                          

def find_item_by_id_topic_item(id_topic_item):
    "Select tabla Topic_item by id_topic_item, para recuperar el registro entero a borrar"
    topic_item = db.session.execute(
        db.select(Topic_item).filter_by(id_topic_item=id_topic_item)).scalar_one()
    return topic_item

def delete_topic_item(topic_item):
    "Accion de borrado del registro de topic_item"
    with transactional_session() as session:
        session.delete(topic_item)
       
def show_result_multiple(id_topic):
    "Muestra los resultados de las votaciones para el topic multiple choice text"
    # Recuperamos lista de respuestas posibles:
    # Haremos un acceso a BBDD Topic_item by id para recuperar todos los items de ese id que serán las posibles respuestas
    topic_item = get_topic_item_by_id_topic(id_topic)
    # inicializamos una lista que vamos a crear de objetos tipo Answer, cada answer tenemos emoji vacío, el order, text y count
    list_answers = []
    for i in topic_item:
        answer = Answer(" ",i.id_order,i.text_answers,0)
        list_answers.append(answer)
        #esto nos devuelve
        #0:Answer(emoji=' ', order=1, text='Lunes, Miercoles', count=0)
        #1:Answer(emoji=' ', order=2, text='Miércoles, Jueves', count=0)
        #2:Answer(emoji=' ', order=3, text='Días alternos', count=0)
        #3:Answer(emoji=' ', order=4, text='Me da igual', count=0)
    #Reuperamos el campo answer directamente en la query y creamos una lista
    list_voted_answers = [i for i in get_answer_by_id(id_topic)]    
    #esto nos devuelve ['1, 3', '1, 4', '2, 3']
    #voted_answers va a tener una lista con los valores de list_voted_answers formateados a enteros
    voted_answers= []
    # Recorrer cada cadena en la lista original
    for cadena in list_voted_answers:
        # Dividir la cadena en elementos individuales
        elementos = cadena.split(',')  
        for elemento in elementos:
           numero = int(elemento)  
           voted_answers.append(numero) 
           #esto nos devuelve [1,3,1,4,2,3]
    #el método update_answers_count actualiza el count de la lista list_answers a partir de las respuestas recogidas
    # en la lista voted_answers       
    list_answers = update_answers_count(voted_answers, list_answers)
    
    return list_answers