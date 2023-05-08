from dataclasses import dataclass
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, or_, select
from alabar.models import Topic, Topic_ticket


# Set up the database connection (NO ES IGUAL A FLASK. NO ESTAMOS EN UN PROCESO DE FLASK AHORA!!!!)
engine = create_engine('sqlite:///./instance/alabar.db')

# Create a new session factory
Session = sessionmaker(bind=engine)
session = Session()

def get_topics_by_user(user_id):
    h = select(Topic_ticket.topic_id).where(Topic_ticket.user_id == user_id)

    stmt = select(Topic).where(
                (Topic.id_owner == user_id) |
                (Topic.id_topic.in_(h))
            )

    s = select(Topic)\
    .where(Topic.deleted_date == '9999-12-31 00:00:00.000000')\
    .where(or_(Topic.id_owner == user_id, Topic.id_topic.in_(h)))
    print(s)
    topics_by_user_list = session.execute(s).scalars().all()
    return topics_by_user_list

@dataclass
class Topic_Answer_Mock:
    id_topic_answer: int
    id_topic: int
    answer: str