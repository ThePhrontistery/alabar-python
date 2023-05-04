from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, delete, or_, select, update
from alabar.models import Topic, Topic_ticket

# Set up the database connection (NO ES IGUAL A FLASK. NO ESTAMOS EN UN PROCESO DE FLASK AHORA!!!!)
engine = create_engine('sqlite:///./instance/alabar.db')

# Create a new session factory
Session = sessionmaker(bind=engine)


def get_topics_by_nuestro(user_id):
    h = select(Topic_ticket.topic_id).where(Topic_ticket.user_id == user_id)

    stmt = select(Topic).where(
                (Topic.id_owner == user_id) |
                (Topic.id_topic.in_(h))
            )

    s = select(Topic)\
    .where(Topic.close_date == '9999-12-31 00:00:00.000000')\
    .where(or_(Topic.id_owner == user_id, Topic.id_topic.in_(h)))

    print(h)
    print(stmt)
    result = session.execute(s).scalars().all()
    return result

if __name__ == '__main__':
    session = Session()
    result = get_topics_by_nuestro('1')
    print(result)