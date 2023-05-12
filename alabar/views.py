import datetime
from flask import Blueprint, redirect, render_template, request, session, url_for

from alabar.data import get_topic_by_id, get_topic_ticket_by_topic_and_user, get_topics_by_user_and_owner, get_user_by_code, get_user_by_id, save_results, save_topic_results, show_result, topic_delete, topic_reopen, typetopics
from alabar.models import Topic_data



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
    return render_template('newtopic.html', typetopics=typetopics)

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
    topic = Topic_data(title_topic=title_topic,id_owner=user.id_user,type_topic=typetopic,
                       end_date=end_date)
    #1.4 save_topic_results (estando en pantalla NEW TOPIC,al dar al botón SAVE se graba en BBDD) -> True o False 
    # Tiene los metodos 'create_topic' y  'create_topic_item'
    # Si ha grabado bien, vuelve a la funcion index para volver a mostrar la tabla de topic actualizada
    if save_topic_results(topic):
    #    if typetopic == 'RatingTopic':
        return redirect(url_for('alabar.index'))
    #    else:
    #       return redirect(url_for('alabar.newtopicitem')) 
    else:
        return render_template('error.html', error_message="error", error_description="No se ha podido grabar su respuesta, inténtelo más tarde")

@alabar_bp.route('/alabar/newtopicitem', methods=['GET'])
def newtopicitem():
    """Pasar a la plantilla de newtopicitem.html los tipos de topic""" 
    return render_template('newtopicitem.html', )