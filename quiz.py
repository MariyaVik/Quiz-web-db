# # Здесь будет код веб-приложения

from flask import Flask, redirect, url_for, session, request, render_template
import random
from db_scripts import get_question_after, get_quizes
import os

def init_session():
    session['question_id'] = 0
    session['quiz_id'] = 0
    session['count_rigth'] = 0
    session['total_count'] = 0
    session['current_answer'] = ''

def select_quiz_form():
    q_list = get_quizes()
    return render_template('start.html', q_list=q_list)


def question_template(question_tuple):
    question = question_tuple[1]
    session['current_answer'] = question_tuple[2]
    answer_list = [question_tuple[2], question_tuple[3],question_tuple[4],question_tuple[5]]
    random.shuffle(answer_list)
    return render_template('test.html', question=question, answers_list=answer_list)

def save_answer():
    user_answer = request.form.get('ans_text')
    if user_answer == session['current_answer']:
        session['count_rigth'] += 1
    session['total_count'] += 1


def index():
    if request.method == 'GET':
        init_session()
        return select_quiz_form()
    else:
        session['quiz_id'] = request.form.get('quiz')
        return redirect(url_for('test'))

def test():
    if 'quiz_id' in session:
        if request.method == 'POST':
            save_answer()
            print('Всего ответов: ', session['total_count'])
            print('Верных ответов: ', session['count_rigth'])

        result = get_question_after(session['question_id'], session['quiz_id'])
        print(result)
        if result is None or len(result) == 0:
            return redirect(url_for('finish'))
        else:
            session['question_id'] = result[0]
            return question_template(result)
    else:
        return redirect(url_for('index'))

def finish():
    return render_template('result.html', count_right=session['count_rigth'], total_count=session['total_count'])

folder = os.getcwd()

app = Flask(__name__, template_folder=folder, static_folder=folder) # создаём объект веб-приложения

app.add_url_rule('/', 'index', index, methods=['post', 'get'])
app.add_url_rule('/test', 'test', test, methods=['post', 'get'])
app.add_url_rule('/finish', 'finish', finish)

app.config['SECRET_KEY'] = 'ThisIsTheMostSecretString'

if __name__ == "__main__":
    app.run()  # запускаем веб-сервер

