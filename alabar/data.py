from .models import User, Group, Topic, Topic_item, Topic_ticket, db

def get_user_by_name(user_name):
    return db.session.execute(db.select(User).filter_by(name_user=user_name)).scalar_one_or_none()

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
