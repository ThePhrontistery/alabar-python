from dataclasses import dataclass
from typing import List
import numpy as np
from alabar.data import get_topic_answers_by_topic_id
from alabar.models import Topic_answer


def show_result(id_topic):
    answers_text = get_answers_text()
    answers = get_topic_answers_by_topic_id(id_topic)
    average = get_average(answers)

    results = Stat(answers_text, answers, average)
    return results


def get_answers_text():
    a = Answer("😭", 1, "very sad")
    b = Answer("🙁", 2, "sad")
    c = Answer("😐", 3, "neutral")
    d = Answer("😊", 4, "happy")
    e = Answer("😃", 5, "very happy")
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



@dataclass
class Answer:
    emoji: str
    order: int
    text: str

@dataclass
class Stat:
    answers_text: List[Answer]
    answers: List[Topic_answer]
    average: int

