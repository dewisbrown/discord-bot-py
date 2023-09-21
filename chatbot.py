'''Saves user input into JSON to use for answers.'''

import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    '''Returns a dictionary of the loaded knowledge_base.json file.'''
    with open(file_path, 'r', encoding='utf-8') as file:
        data: dict = json.load(file)
    return data


def save_knowledge_base(file_path: str, data: dict):
    '''Saves new questions and answers to the knowledge_base.json file.'''
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    '''Finds a close match to the user question from a list of questions.'''
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    '''Returns answer for a given question from the knowledge base.'''
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]


def chatbot_interface(user_input: str) -> str | None:
    '''Retrieves answer from knowledge_base.json. If no answer, inputs new answer from user.'''
    knowledge_base: dict = load_knowledge_base('data/knowledge_base.json')
    best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    if best_match:
        return get_answer_for_question(best_match, knowledge_base)
    else:
        return None


def add_new_answer(question: str, answer: str):
    '''Adds question and answer to knowledge_base.json.'''
    knowledge_base: dict = load_knowledge_base('data/knowledge_base.json')
    knowledge_base["questions"].append({"question": question, "answer": answer})
    save_knowledge_base('data/knowledge_base.json', knowledge_base)
