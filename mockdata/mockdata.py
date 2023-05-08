from dataclasses import dataclass
from typing import List
import numpy as np
from alabar.data import get_topic_answers_by_topic_id
from alabar.models import Topic_answer


def show_result(id_topic):
    answers_text = get_answers_text()
    answers = get_topic_answers_by_topic_id(id_topic)
    average = round(get_average(answers))

    # ESTO ES MUY FEO? HAY UNA MEJOR MANERA DE HACERLO?
    #average_text = [answer_text for answer_text in answers_text if average == answer_text.order][0]
    answers_text = get_answers_count(answers, answers_text)
    average_text = answers_text[0]
    for i in (answer_text for answer_text in answers_text if average == answer_text.order):
        average_text = i
        
    results = Stat(answers_text, average_text)
    return results

def get_answers_text():
    a = Answer("😭", 1, "very sad", 1)
    b = Answer("🙁", 2, "sad", 2)
    c = Answer("😐", 3, "neutral", 3)
    d = Answer("😊", 4, "happy", 0)
    e = Answer("😃", 5, "very happy", 0)
    answers = [a, b, c, d, e]
    return answers

def get_average(answers):
    answers_list = [int(answer.answer) for answer in answers]
    answers_count = len(answers_list)
    unique_answers_list = get_unique_answers(answers_list)
    answers_sum = 0
    for voted_answer in unique_answers_list:
        voted_answer_count = sum(map(lambda i: i == voted_answer, answers_list))
        answers_sum = answers_sum + voted_answer * voted_answer_count
    average = answers_sum/answers_count
    return average

def get_unique_answers(answers_list):
    x = np.array(answers_list)
    return np.unique(x).tolist()

def get_answers_count(answers, answers_text):
    for i in len(answers):
        count = sum(elem.answer == i (elem) for elem in answers)
    return answers_text




@dataclass
class Answer:
    emoji: str
    order: int
    text: str
    count: int

@dataclass
class Stat:
    answers_text: List[Answer]
    answer_text: Answer

@dataclass
class Topic_Answer_Mock:
    id_topic_answer: int
    id_topic: int
    answer: str

