from mockdata.mockdata import Topic_Answer_Mock, get_topics_by_user
from alabar.data import get_topic_item_by_id_topic

def get_topic_answers(id_topic):
    topic_answer_list = [Topic_Answer_Mock(1, id_topic, '3'),
                         Topic_Answer_Mock(2, id_topic, '1'),
                         Topic_Answer_Mock(3, id_topic, '2'),
                         Topic_Answer_Mock(4, id_topic, '3')]
    return topic_answer_list





if __name__ == '__main__':
    #topics_by_user_list = get_topics_by_user('1')

    #topic_answer_list = get_topic_answers(3)

    id_topic = 8
    id_order_max = get_topic_item_by_id_topic(id_topic)
    print(id_order_max)



    print(bool(0))
    print(bool(1))
