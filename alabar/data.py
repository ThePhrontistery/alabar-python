from .models import User, Group, Topic, Topic_item, Topic_ticket, db

def get_user_by_name(user_name):
    return db.session.execute(db.select(User).filter_by(name_user=user_name)).scalar_one_or_none()

def get_user_by_id(id_user):
    return db.session.execute(db.select(User).filter_by(id_user=id_user)).scalar_one_or_none()

def get_user_by_code(code_user):
    return db.session.execute(db.select(User).filter_by(code_user=code_user)).scalar_one_or_none()

def get_topic_ticket_by_id(user_id):
    "Select tabla Topic_ticket by user_id"
    #return db.session.execute(db.select(Topic_ticket).filter_by(name_user=user_name)).scalar_one_or_none()
    return db.session.execute(db.select(Topic_ticket)
                              .where(Topic_ticket.user_id == user_id)).scalars().all()

def get_topics_by_user(user_id):
    "Get topic (must exist) associated users"
    topic_ticket = get_topic_ticket_by_id(user_id)
    topics_users = []
    for i in topic_ticket:
        topics_users.append(i.topics) 
    return topics_users

def get_topics_by_owner(user_id):
    #Select Topic by id_owner
    return db.session.execute(db.select(Topic).where(Topic.id_owner == user_id)).scalars().all()

#def get_topics_by_nuestro(user_id):
#    s = select([Topic]).where(Topic.date == '9999-12-31 00:00:00.000000' & Topic.id_owner = user_id or Topic.id_topic in select Topic_ticket.topic_id from Topic_ticket where Topic_ticket.user_id = user_id))
#    result = db.execute(s)
#    print(result)
#    return result