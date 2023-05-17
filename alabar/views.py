import datetime
from flask import Blueprint, redirect, render_template, request, session, url_for

from alabar.data import delete_topic_item, find_item_by_id_topic_item, get_id_topic_by_data, get_max_id_order_in_topic_item, get_topic_by_id, get_topic_item_by_id_topic, get_topic_ticket_by_topic_and_user, get_topics_by_user_and_owner, get_user_by_code, get_user_by_id, save_results, save_results_item, save_topic_results, show_result, topic_delete, topic_reopen, typetopics, get_id_topic_by_data
from alabar.models import Topic, Topic_data



alabar_bp = Blueprint('alabar', __name__)


#@alabar.route('/', methods=['POST'])
@alabar_bp.route('/alabar')
def index():
    """Recuperamos tabla de topics""" 
    #Se recuperan los topics de topic_ticket, topics que puede responder y topics que administra
    user = get_user_by_code(session['CURRENT_USER'])
    table_topics = get_topics_by_user_and_owner(user.id_user)
    current_date = datetime.datetime.now()

    # Reemplazo el contenido de id_owner por el name_user
    for table_topic in table_topics:
        table_topic.id_owner = get_user_by_id(table_topic.id_owner).name_user
    return render_template('index.html', table_topics=table_topics,current_date=current_date)

@alabar_bp.route('/alabar/rating', methods=['GET', 'POST'])
def rating():
    "recuperar topic por id para comprobar el estado y recuperar topic ticket para comprobar si el user ha completado el topic"
    #TODO: ver porque no funciona el POST en el formulario, ahora estamos recuperando por url (posible problema de seguridad) 
    # id_topic = request.form['topic_id']

    id_topic = request.args.get('topic_id')
    topic = get_topic_by_id(id_topic)
    user = get_user_by_code(session['CURRENT_USER'])
    topic_ticket = get_topic_ticket_by_topic_and_user(id_topic, user.id_user)
    current_date = datetime.datetime.now().date()
    db_end_date = topic.end_date.date()

    results = 0
    if topic.status == False or current_date >= db_end_date:
        results = show_result(id_topic)

    return render_template('rating.html', topic=topic, topic_ticket=topic_ticket, results=results, current_date=current_date, db_end_date=db_end_date)



@alabar_bp.route('/alabar/rating_results', methods=['POST'])
def rating_results():
    """Actualizacion en BBDD los resultados del topic rating_results""" 
    #1.1 Obtenemos datos de pantalla con request.form (topic_id y radio -rating-)
    id_topic = request.form['topic_id']
    rating = request.form['emoji']

    #1.2 Creamos answers como un diccionario con clave de 1 a 5 (para cada emoticono) y asignando valor 1 al que tenga valor
    # en lo recibido en rating (value de 'radio')
    #answers = {'1':0, '2':0, '3':0, '4':0, '5':0}
    #if rating in answers:
    #    answers[rating] = 1 
    answer = rating
    
    #1.3 save_results (estando en pantalla RESULT,al dar al botón SAVE se graba en BBDD) -> True o False 
    # Tiene los metodos 'create_answer', 'update_ticket' y 'update_topic'
    # Si ha grabado bien, vuelve a la funcion index para volver a mostrar la tabla de topic actualizada
    if save_results(id_topic,answer, session['CURRENT_USER']):
        return redirect(url_for('alabar.index'))
    else:
        return render_template('error.html', error_message="error", error_description="No se ha podido grabar su respuesta, inténtelo más tarde")

@alabar_bp.route('/alabar/reopen', methods=['GET'])
def reopen():
    id_topic = request.args.get('topic_id')
    if topic_reopen(id_topic):
        return redirect(url_for('alabar.index'))
    else:
        return render_template('error.html', error_message="error", error_description="No se ha podido reabrir, inténtelo más tarde")


@alabar_bp.route('/alabar/delete', methods=['GET'])
def delete():
    id_topic = request.args.get('topic_id')
    if topic_delete(id_topic):
        return redirect(url_for('alabar.index'))
    else:
        return render_template('error.html', error_message="error", error_description="No se ha podido eliminar, inténtelo más tarde")

@alabar_bp.route('/alabar/newtopic', methods=['GET'])
def newtopic():
    """Pasar a la plantilla de newtopic.html los tipos de topic""" 
    # Creamos objeto topic de la clase Topic, inicializado 
    topic = Topic()
    # La primera vez que va al html el topic no esta creado (entra en la primera parte)
    return render_template('newtopic.html', typetopics=typetopics,topic=topic)

@alabar_bp.route('/alabar/save_topic', methods=['POST'])
def save_topic():
    """Actualizacion en BBDD los resultados de salvar el topic""" 
    #1.1 Obtenemos datos de pantalla con request.form (titulo,fecha fin,tytopic seleccionado)
    title_topic = request.form['title_topic']
    # end_date recuperada del formulario es tipo str y tiene formato AAAA-MM-DDTHH:MM:SS.
    # hay que convertirlo a objeto datetime.datetime (con strptime) y a formato AAAA-MM-DD HH:MM:SS
    if request.form['end_date']:
       end_date= datetime.datetime.strptime(request.form['end_date'], "%Y-%m-%dT%H:%M")
    else:
       end_date = datetime.datetime.strptime('9999-12-31 00:00:00', "%Y-%m-%d %H:%M:%S")
    typetopic = request.form['typetopic']
    #1.2 del user_code conectado recuperamos su id.user
    user = get_user_by_code(session['CURRENT_USER'])
    #1.3 Creamos objeto topic de la clase Topic_data para pasar todos los parametros que necesita para crear topic
    topic_data = Topic_data(title_topic=title_topic,id_owner=user.id_user,type_topic=typetopic,
                       end_date=end_date)
    #1.4 save_topic_results (estando en pantalla NEW TOPIC,al dar al botón SAVE se graba en BBDD) -> True o False 
    # Tiene los metodos 'create_topic' y  'create_topic_item'
    # Si ha grabado bien, vuelve a la funcion index para volver a mostrar la tabla de topic actualizada
    topic_select = save_topic_results(topic_data)
    if topic_select:
        topic = get_id_topic_by_data(topic_select)
        if typetopic == 'RatingTopic':
           return redirect(url_for('alabar.index'))
        else:
           #return render_template('newtopicitem.html', id_topic=topic.id_topic ) 
           # Si ya se ha creado el topic, vamos al html a la segunda parte (crear topic_item)
           return render_template('newtopic.html',typetopics=typetopics,topic=topic) 
    else:
        return render_template('error.html', error_message="error", error_description="No se ha podido grabar su respuesta, inténtelo más tarde")


@alabar_bp.route('/alabar/add_item', methods=['POST'])
def add_item():
    """Actualizacion en BBDD los resultados del topic_item""" 
    #1.1 Obtenemos datos de pantalla con request.form (id_topic y el item añadido)
    id_topic = request.form['id_topic']
    text_answers = request.form['text_answers']
    
    #1.2 Calculo de id_order 
    # Select tabla Topic_item by id_topic, para recuperar el id order maximo para cada id_topic
    id_order_max = get_max_id_order_in_topic_item(int(id_topic))
    # Si no devuelve nada, es que no existe ningun item en topic_item, será el primero
    if id_order_max == None:
         id_order = 1
    else:
         id_order = id_order_max + 1

    #1.3 save_results_item (al dar al botón SAVE se graba en BBDD de topic_item) -> True o False 
    # Tiene el metodo 'create_topic_item'
    # Si ha grabado bien, actualiza la lista de topic_item para el id_topic
    if save_results_item(id_topic, id_order,text_answers):
        return render_items(id_topic)
    else:
        return render_template('error.html', error_message="error", error_description="No se ha podido grabar su respuesta, inténtelo más tarde")


def render_items(id_topic):
    """Metodo que presenta la lista de topic_item actualizada con template""" 
    #Select tabla Topic_item by id_topic, para recuperar todos los topic_item
    items = get_topic_item_by_id_topic(id_topic)
    return render_template('items.html', items=items)

@alabar_bp.route('/alabar/delete_item', methods=['POST'])
def delete_item():
    """Actualizacion en BBDD (topic_item) al dar al botón borrar el item introducido""" 
    id_topic_item = int(request.form['id_topic_item'])
    # Select tabla Topic_item by id_topic_item, para recuperar el registro entero a borrar
    topic_item = find_item_by_id_topic_item(id_topic_item)
    # Para volver a presentar los topic_item del id_topic necesitamos tenerlo (para el render_item)
    id_topic = topic_item.id_topic
    # Accion de borrado del registro de topic_item
    delete_topic_item(topic_item)
    return render_items(id_topic)


@alabar_bp.route('/alabar/multiple_choice_text', methods=['GET', 'POST'])
def multiple_choice_text():
    "recuperar topic por id para comprobar el estado y recuperar topic ticket para comprobar si el user ha completado el topic y recuperar topic_item"
    
    id_topic = request.args.get('topic_id')
    #Se recupera un objeto Topic por id_topic
    topic = get_topic_by_id(id_topic)
    #Se recupera el objeto de tipo User, lo necesitamos para acceder a topic_ticket
    user = get_user_by_code(session['CURRENT_USER'])
    #Se accede a topic_ticket para saber si ha contestado al topic
    topic_ticket = get_topic_ticket_by_topic_and_user(id_topic, user.id_user)
    current_date = datetime.datetime.now().date()
    db_end_date = topic.end_date.date()

    #Se accede a topic_item para recuperar las respuestas que se muestran en pantalla
    topic_item = get_topic_item_by_id_topic(id_topic)

    results = 0
    if topic.status == False or current_date >= db_end_date:
        results = show_result(id_topic)

    return render_template('MultipleChoiceText.html', topic=topic, topic_ticket=topic_ticket, results=results, current_date=current_date, db_end_date=db_end_date, topic_items=topic_item)

@alabar_bp.route('/alabar/mct_results', methods=['POST'])
def mct_results():
    """Actualizacion en BBDD los resultados del topic multiple choice text""" 
    #1.1 Obtenemos datos de pantalla con request.form (topic_id y radio -rating-)
    id_topic = request.form['topic_id']
    rating = request.form['item-0']

    #1.2 Creamos answers como un diccionario con clave de 1 a 5 (para cada emoticono) y asignando valor 1 al que tenga valor
    # en lo recibido en rating (value de 'radio')
    #answers = {'1':0, '2':0, '3':0, '4':0, '5':0}
    #if rating in answers:
    #    answers[rating] = 1 
    answer = rating
    
    #1.3 save_results (estando en pantalla RESULT,al dar al botón SAVE se graba en BBDD) -> True o False 
    # Tiene los metodos 'create_answer', 'update_ticket' y 'update_topic'
    # Si ha grabado bien, vuelve a la funcion index para volver a mostrar la tabla de topic actualizada
    if save_results(id_topic,answer, session['CURRENT_USER']):
        return redirect(url_for('alabar.index'))
    else:
        return render_template('error.html', error_message="error", error_description="No se ha podido grabar su respuesta, inténtelo más tarde")