# telegram_bot/models/task_4_model.py

import json
import random
import os

def load_words():
    base_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'task_4')
    correct_path = os.path.join(base_path, 'correct.json')
    incorrect_path = os.path.join(base_path, 'incorrect.json')
    try:
        with open(correct_path, 'r', encoding='utf-8') as f:
            correct = json.load(f)
        with open(incorrect_path, 'r', encoding='utf-8') as f:
            incorrect = json.load(f)
    except Exception as e:
        raise RuntimeError(f"Ошибка загрузки слов: {e}")
    return correct, incorrect

def generate_question(context):
    correct, incorrect = load_words()
    n = random.randint(1, 4)
    selected_correct = []
    selected_incorrect = []
    correct_pool = correct.copy()
    incorrect_pool = incorrect.copy()
    while len(selected_correct) < n and correct_pool:
        available = [word for word in correct_pool if word.lower() not in {w.lower() for w in selected_correct}]
        if not available:
            break
        word = random.choice(available)
        selected_correct.append(word)
        correct_pool.remove(word)
    while len(selected_incorrect) < (5 - n) and incorrect_pool:
        available = [word for word in incorrect_pool if word.lower() not in {w.lower() for w in (selected_correct + selected_incorrect)}]
        if not available:
            break
        word = random.choice(available)
        selected_incorrect.append(word)
        incorrect_pool.remove(word)
    all_words = selected_correct + selected_incorrect
    random.shuffle(all_words)
    context.user_data['current_question'] = {
        'words': all_words,
        'correct_indices': [i for i, word in enumerate(all_words) if word in selected_correct]
    }
    
def get_correct_answer(question):
    return ''.join(str(i+1) for i in sorted(question['correct_indices']))
