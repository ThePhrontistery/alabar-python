from dataclasses import dataclass


def show_result(id_topic):
    stat = {}
    total_answer = len(stat)
    return total_answer, stat


def get_answers(id_topic):
    a = Answer("😭", 1, 0, "very sad")
    b = Answer("🙁", 2, 1, "sad")
    c = Answer("😐", 3, 0, "neutral")
    d = Answer("😊", 4, 1, "happy")
    e = Answer("😃", 5, 0, "very happy")
    answers = [a, b, c, d, e]
    return answers

def get_average(answers):
    answers = get_answers(1)
    list = []
    for answer in answers:
        list.append(answer.order * answer.value) 
    answer_sum = sum(i for i in list)
    total_answers = sum(1 for i in answers if i.value > 0)
    average = answer_sum/total_answers
    return average



@dataclass
class Answer:
    emoji: str
    order: int
    value: int
    text: str

@dataclass
class Stat:
    answer: Answer
    average: int
    value: int