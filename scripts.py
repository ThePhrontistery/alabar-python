from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, delete, or_, select, update
from alabar.models import Topic, Topic_ticket
from mockdata.mockdata import Answer, Topic_Answer_Mock, get_answers_text, get_average
import numpy as np

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


def get_answers_count(answers, answers_text):
    for i in range(len(answers)):
        count = sum(elem.answer == i (elem) for elem in answers)
    return answers_text

def get_unique_answers(answers_list):
    x = np.array(answers_list)
    return np.unique(x).tolist()

if __name__ == '__main__':
    # session = Session()
    # # result = get_topics_by_nuestro('1')
    # answers_text = get_answers_text()
    # average = round(9)
    # average = round(9)
    # topic_answer_list = [Topic_Answer_Mock(1, 3, '1'),Topic_Answer_Mock(2, 3, '3'),Topic_Answer_Mock(3, 3, '2'),Topic_Answer_Mock(4, 3, '2')]
    # answers_list = [int(answer.answer) for answer in topic_answer_list] #[3, 3, 2, 2]
    # answers_list = [1, 3, 2, 2]

    # x = np.array(answers_list)
    # for i in answers_text:
    #     i.count = (x == i.order).sum()
    #     print(i.count)

    # answers_count = len(answers_list)
    # a = get_unique_answers(topic_answer_list)
    # get_answers_count(topic_answer_list, answers_text)
    if 0:
        print('ok')

    # print(topic_answer_list)