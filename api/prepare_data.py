# для ВМ

# запись вероятностей принадлжености к классу
# модуль предобработки данных о резюме
# для автомодерации с внедрением API.
# на вход подается одна строка фрейма со множеством столбцов,
# на выходе получается фрейм с одной строкой и одним столбцом,
# который получается в ходе преобразования столбцов к строковой форме

import os
import re

import nltk
import pymorphy2
import pandas as pd

from nltk.corpus import stopwords
from catboost import CatBoostClassifier


nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('russian'))


def create_model():
    model = CatBoostClassifier()
    return model

def predict_X(X):
    path_model = "../api/"
    file_model = "hack_model.uu"
    model = create_model()
    model.load_model(os.path.join(path_model, file_model))
    y_pred = int(model.predict(X)[0])
    y_proba = model.predict_proba(X)[0]
    y_proba = y_proba[y_pred]
    print("y_pred ", y_pred, ". y_proba ", y_proba)
    return [y_pred, y_proba]

def en_to_run(string):
    en_ru = {'A': 'А', 'a': 'а', 'B': 'Б', 'b': 'б', 'V': 'В', 'v': 'в',
    'G': 'Г', 'g': 'г', 'D': 'Д', 'd': 'д', 'E': 'Э', 'e': 'э', 'Yo': 'Ё', 'yo': 'ё',
    'Zh': 'Ж', 'zh': 'ж', 'Z': 'З', 'z': 'з', 'I': 'И', 'i': 'и', 'Y': 'Й', 'y': 'й',
    'K': 'К', 'k': 'к', 'L': 'Л', 'l': 'л', 'M': 'М', 'm': 'м', 'N': 'Н', 'n': 'н',
    'O': 'О', 'o': 'о', 'P': 'П', 'p': 'п', 'R': 'Р', 'r': 'р', 'S': 'С', 's': 'с',
    'T': 'Т', 't': 'т', 'U': 'У', 'u': 'у', 'F': 'Ф', 'f': 'ф', 'H': 'Х', 'h': 'х',
    'Ts': 'Ц', 'ts': 'ц', 'Ch': 'Ч', 'ch': 'ч', 'Sh': 'Ш', 'sh': 'ш', 'Sch': 'Щ', 'sch': 'щ',
    'Yi': 'Ы', 'yi': 'ы', 'Yu': 'Ю', 'yu': 'ю', 'Ya': 'Я', 'ya': 'я'}

    for k, v in en_ru.items():
        if k in string:
            string = string.replace(k, v)
    
    return string.lower().strip()

def clear_text(string):
    new_string = re.sub('[^а-яА-Я]', '', string)
    return re.sub('\s+',' ', new_string)

# приведение токенов входящих в текст к нормальной форме
def norm(text):
    morph = pymorphy2.MorphAnalyzer()
    text_norm = ''
    for token in nltk.word_tokenize(text):
        # print('token = ', token)
        token_norm = morph.parse(token)[0].normal_form
        if token_norm not in stop_words:
            text_norm = text_norm + ' ' + token_norm
        # print('text_norm', text_norm)
    return text_norm

def text_clear(text):
    text = clear_text(en_to_run(text))
    text = norm(text)
    return text

def main_clear(data_json):        
    text = text_clear(data_json["comment"])
    return text

def main_predict(data_json):
    X = main_clear(data_json)
    X = pd.DataFrame(data={"text": [X]})
    code = predict_X(X)

    ans = {
        'event_type': data_json['event_type'],
        'body': {
            "answer": "toxic" if code[0] == 1 else "not toxic",
            "probability": code[1]
        }
    }
    return ans
