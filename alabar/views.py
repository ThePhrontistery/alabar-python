from typing import List
import datetime
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for

from alabar.data import delete_table_usergroup, delete_topic_item, delete_topic_ticket, find_item_by_id_topic_item, find_ticket_by_id_topic, get_groups, get_id_topic_by_data, get_max_id_order_in_topic_item, get_topic_by_id, get_topic_item_by_id_topic, get_topic_ticket_by_topic, get_topic_ticket_by_topic_and_user, get_topics_by_user_and_owner, get_user_by_code, get_user_by_id, get_user_by_name, get_users, get_users_by_id_group, save_results, save_results_item, save_results_user, save_results_usergroup, save_topic_results, show_result, show_result_multiple, topic_close, topic_delete, topic_reopen, typetopics, get_id_topic_by_data
from alabar.models import Group, Topic, Topic_data, Topic_ticket, Topic_ticket_user, User



alabar_bp = Blueprint('alabar', __name__)


#@alabar.route('/', methods=['POST'])
@alabar_bp.route('/alabar')
def index():
    """Recuperamos tabla de topics""" 
    #Se recuperan los topics de topic_ticket, topics que puede responder y topics que administra
    user = get_user_by_code(session['CURRENT_USER'])
    table_topics = get_topics_by_user_and_owner(user.id_user)
    current_date = datetime.datetime.now() #-> sacaria formato datetime.datetime(2023, 5, 19, 13, 55, 13, 957567)

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
    #en answer vamos a guardar el valor del emoticono seleccionado
    answer = rating
    
    #1.3 save_results (estando en pantalla RESULT,al dar al botón SAVE se graba en BBDD) -> True o False 
    # Tiene los metodos 'create_answer', 'update_ticket' y 'update_topic'
    # Si ha grabado bien, vuelve a la funcion index para volver a mostrar la tabla de topic actualizada
    if save_results(id_topic,answer, session['CURRENT_USER']):
        return redirect(url_for('alabar.index'))
    else:
        return render_template('error.html', error_message="error", error_description="Your response could not be saved, please try again later")

@alabar_bp.route('/alabar/reopen', methods=['GET'])
def reopen():
    """desde el listado de topic, dan al botón de reopen""" 
    id_topic = request.args.get('topic_id')
    # topic es objeto de la clase Topic con el registro del id_topic seleccionado
    topic = get_topic_by_id(id_topic)
    if topic:
        return render_template('modifytopic.html', topic=topic)
    else:
        return render_template('error.html', error_message="error", error_description="Failed to reopen the topic, please try again later")


@alabar_bp.route('/alabar/modify_topic', methods=['POST'])
def modify_topic():
    """Actualizacion en BBDD los resultados de la modificacion de end_date y del status del topic al dar a reopen""" 
    #1.1 Obtenemos datos de pantalla con request.form (topic_id)
    id_topic = request.form['id_topic']
    # end_date recuperada del formulario es tipo str y tiene formato AAAA-MM-DDTHH:MM:SS.
    # hay que convertirlo a objeto datetime.datetime (con strptime) y a formato AAAA-MM-DD HH:MM:SS
    end_date= datetime.datetime.strptime(request.form['end_date'], "%Y-%m-%dT%H:%M")
    #Estando en pantalla de Modify Topic end_date, ha modifcado end_date y da a save y se actualiza end_date y status a True
    if topic_reopen(id_topic,end_date):
        return redirect(url_for('alabar.index'))
    else:
        return render_template('error.html', error_message="error", error_description="Your response could not be saved, please try again later")


@alabar_bp.route('/alabar/delete', methods=['GET'])
def delete():
    id_topic = request.args.get('topic_id')
    if topic_delete(id_topic):
        return redirect(url_for('alabar.index'))
    else:
        return render_template('error.html', error_message="error", error_description="The topic could not be deleted, please try again later")

@alabar_bp.route('/alabar/newtopic', methods=['GET'])
def newtopic():
    """Pasar a la plantilla de newtopic.html los tipos de topic""" 
    # Creamos objeto topic de la clase Topic, inicializado 
    topic = Topic()
    #inicializamos usersgroup que es un objeto de la clase User  
    usersgroup = Group().users
    #inicializamos groups que es un objeto de la clase Group  
    groups = Group()
    #inicializamos users_list que es un objeto de la clase User  
    users_list = User()
    # La primera vez que va al html el topic no esta creado (entra en la primera parte)
    return render_template('newtopic.html', typetopics=typetopics,topic=topic, usersgroup=usersgroup, groups=groups,mensajeerror="",users_list=users_list)

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
        #groups es objeto de clase Group que tiene todos los grupos desde tabla Group. 
        groups = get_groups()
        #si ha encontrado al menos un grupo va a presentar los usuarios del primer grupo de la lista [0]
        #usersgroup es objeto de clase User (a través de la propiedad users de la clase Group)
        if len(groups) > 0:
           usersgroup=groups[0].users
        # users_list es un objeto de la clase Users que muestra en un desplegable la lista de usuarios posibles
        users_list= get_users()
        return render_template('newtopic.html',typetopics=typetopics,topic=topic, usersgroup=usersgroup, groups=groups, mensajeerror="", users_list=users_list) 
    else:
        return render_template('error.html', error_message="error", error_description="Your response could not be saved, please try again later")


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
        return render_template('error.html', error_message="error", error_description="Your response could not be saved, please try again later")


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
       results = show_result_multiple(id_topic)

    return render_template('MultipleChoiceText.html', topic=topic, topic_ticket=topic_ticket, results=results, current_date=current_date, db_end_date=db_end_date, topic_items=topic_item)

@alabar_bp.route('/alabar/mct_results', methods=['POST'])
def mct_results():
    """Actualizacion en BBDD los resultados del topic multiple choice text""" 
    #1.1 Obtenemos datos de pantalla con request.form (topic_id y radio -rating-)
    id_topic = request.form['topic_id']
    #rating = request.form['item-0']
    selected_items = request.form.getlist("selected_item[]")
    #answer = {valor: indice for indice, valor in enumerate(selected_items)}
    #con join paso a string la lista de los items seleccionados para grabarlo en BBDD
    answer = ', '.join(selected_items)
    #print(answer)
    #1.3 save_results (estando en pantalla RESULT,al dar al botón SAVE se graba en BBDD) -> True o False 
    # Tiene los metodos 'create_answer', 'update_ticket' y 'update_topic'
    # Si ha grabado bien, vuelve a la funcion index para volver a mostrar la tabla de topic actualizada
    if save_results(id_topic,answer, session['CURRENT_USER']):
        return redirect(url_for('alabar.index'))
    else:
        return render_template('error.html', error_message="error", error_description="Your response could not be saved, please try again later")

@alabar_bp.route('/alabar/close', methods=['GET'])
def close():
    id_topic = request.args.get('topic_id')
    if topic_close(id_topic):
        return redirect(url_for('alabar.index'))
    else:
        return render_template('error.html', error_message="error", error_description="Failed to delete, please try again later")

@alabar_bp.route('/alabar/add_user', methods=['POST'])
def add_user():
    """Actualizacion en BBDD los resultados del topic_ticket""" 
    #1.1 Obtenemos datos de pantalla con request.form (id_topic y el nombre de la persona añadido)
    #topic_id = request.args.get("id_topic")
    #user_id = request.args.get("id_user")
    topic_id = request.form['id_topic']
    #name_user = request.form['name_user']
    user_id = request.form['id_user']

    mensajeerror=""

    #1.2. Se recupera el objeto de tipo User, lo necesitamos para acceder a topic_ticket
    #try:
    #    user_id = get_user_by_name(name_user).id_user
    #except:        
    #    mensajeerror = 'Non existent user'        
    #    return render_users(topic_id,mensajeerror)
    
    #1.3 Comprobar que el registro a insertar en topic_ticket no existe
    topic_ticket = get_topic_ticket_by_topic_and_user(topic_id, user_id)
    #Si lo encuntra, muestra error
    #Si no lo encuentra llama a save_results_user (al dar al botón ADD USER se graba en BBDD de topic_ticket)->True o False 
    # Tiene el metodo 'create_topic_user'
    # Si ha grabado bien, actualiza la lista de topic_ticket para el id_topic e id_user
    if topic_ticket != None: 
        mensajeerror = 'Existing user'        
        return render_users(topic_id,mensajeerror)
    else: 
        if save_results_user(user_id,topic_id):
            return render_users(topic_id,mensajeerror)
        else:
            return render_template('error.html', error_message="error", error_description="Your response could not be saved, please try again later")

def render_users(topic_id,mensajeerror):
    """Metodo que presenta la lista de topic_ticket y sus users correspondiente actualizada con template""" 
    #Inicializamos objeto topic_tickets_user de la clase Topic_ticket_user (que tiene subclase Topic_ticket
    # y subclase Users)
    topic_tickets_user = Topic_ticket_user(List[Topic_ticket], List[User])
    #Creo objeto topic_tickets_user.topic_tickets (de la subclase Topic_ticket) que tiene todas las filas
    # de la tabla Topic_ticket de un topic_id dado.
    topic_tickets_user.topic_tickets = get_topic_ticket_by_topic(topic_id)
    #Creo objeto topic_tickets_user.users (de la subclase Users) como una lista inicializada de clase Users
    topic_tickets_user.users = []
    #Recorro la tabla topic_tickets_user.topic_tickets (de tipo subclase Topic_ticket).
    # Para cada fila con el user_id accedo a tabla User (con get_user_by_id, pasando como parametro el user_id), 
    # Con el append voy creando la lista de los users para poder iterar sobre ello en el users.html
    for topic_ticket in topic_tickets_user.topic_tickets:
        topic_tickets_user.users.append(get_user_by_id(topic_ticket.user_id))
    #Como parametros paso topic_tickets_user.users (objeto lista de subclase Users dentro de clase 
    # Topic_ticket_user que tiene los users de ese topic para luego mostrar el name_user) y topic_id
    return render_template('users.html', topic_ticket_user=topic_tickets_user.users,topic_id=topic_id,mensajeerror=mensajeerror)


@alabar_bp.route('/alabar/delete_user', methods=['POST'])
def delete_user():
    """Actualizacion en BBDD (topic_ticket) al dar al botón borrar el user introducido""" 
    topic_id = int(request.form['topic_id'])
    user_id = int(request.form['id_user'])
    # Select tabla Topic_ticket by topic_id y user_id, para recuperar el registro entero a borrar
    topic_ticket = find_ticket_by_id_topic(user_id,topic_id)
    # Para volver a presentar los topic_ticket del id_topic necesitamos tenerlo (para el render_users)
    topic_id = topic_ticket.topic_id
    # Accion de borrado del registro de topic_ticket
    delete_topic_ticket(topic_ticket)
    return render_users(topic_id,mensajeerror="")

@alabar_bp.route('/alabar/usersgroup', methods=['GET'])
def usersgroup():
    """Dentro de newtopic.html presentamos los usuarios del grupo seleccionado""" 
    #pasamos el parámetro de id_group con el grupo seleccionado en el combo
    id_group = request.args.get("id_group")
    return render_usersgroup(id_group)


def render_usersgroup(id_group):
    """Presenta la plantilla usergroup.html con los usuario del grupo seleccionado en el combo""" 
    #usersgroup es un objeto de la clase User que nos retorna get_users_by_id_group (return group.users)
    #en este punto ya no tenemos id_group, porque solo retornamos el objeto de tipo users.
    usersgroup = get_users_by_id_group(id_group)
    return render_template('usersgroup.html', usersgroup=usersgroup)

@alabar_bp.route('/alabar/add_usersgroup', methods=['POST'])
def add_usersgroup():
    """Actualizacion en BBDD los resultados del topic_ticket habiendo añadido grupo""" 
    #1.1 Obtenemos datos de pantalla con request.form (id_topic y el id de grupo añadido)
    topic_id = request.form['id_topic']
    id_group = request.form['id_group']
    
    #1.2. Se recupera el objeto de tipo Group, para acceder a los usuarios que pertenecen a ese grupo    
    #usersgroup es un objeto de la clase User que nos retorna get_users_by_id_group (return group.users)
    #en este punto ya no tenemos id_group, porque solo retornamos el objeto de tipo users.
    try:
        usersgroup = get_users_by_id_group(id_group)           
    except:
        error_description="Your response could not be saved, please try again later"
        return render_users(topic_id,mensajeerror=error_description)
   
    #1.3. Se llama al metodo save_results_usergroup para actualizar topic_ticket   
    # Tiene el metodo 'create_topic_user'
    # Si ha grabado bien, actualiza la lista de topic_ticket para el id_topic e id_user que se encuentren en user_group
    resuts_usersgroup = save_results_usergroup(usersgroup,topic_id)
    #if save_results_usergroup(usersgroup,topic_id):
    if resuts_usersgroup:
        return render_users(topic_id,mensajeerror="")
    else:
        if resuts_usersgroup == None:
            error_description="One of the users in the group already exists, the rest are added"
            return render_users(topic_id,mensajeerror=error_description)
        else: 
            error_description="Failed to record, please try again later"
            return render_users(topic_id,mensajeerror=error_description)
            

@alabar_bp.route('/alabar/delete_usersgroup', methods=['POST'])
def delete_usersgroup():
    """Actualizacion en BBDD (topic_ticket) al dar al botón borrar el group introducido""" 
    topic_id = int(request.form['id_topic'])
    id_group = int(request.form['id_group'])

    # Select tabla user_group by topic_id y group_id, para recuperar los usuarios a borrar
    try:
        usersgroup = get_users_by_id_group(id_group)
    except:
        error_description="Could not delete, please try again later"
        return render_users(topic_id,mensajeerror=error_description)
    
    if usersgroup != None: 
        #Se llama a la función para el borrado de todos los usuarios que tiene el grupo a borrar
        if delete_table_usergroup(usersgroup,topic_id):
            # Para volver a presentar los topic_ticket del id_topic necesitamos tenerlo (para el render_users)        
            return render_users(topic_id,mensajeerror="")
        else:
            error_description="Could not delete, please try again later"
            return render_users(topic_id,mensajeerror=error_description)
            #return render_template('error.html', error_message="error", )

      