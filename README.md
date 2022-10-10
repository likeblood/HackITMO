# hack_itmo
Данные: https://www.kaggle.com/datasets/blackmoon/russian-language-toxic-comments.

В данных есть перекос классов в связи с чем взята метрика `F1`.
Из чего состоит:
1. Предобработка текста(удаление лишних символов, стоп-слов, приведение к нормальной форме - pymorphy2)
2. Обучение с CatBoost(2500 эпох на GPU). `F1 = 84%`
3. API Flask которая так же применяет предобработку текста.

После скачивания репы нужно в ней же создать директорию `data` - там должны быть размещены данные для обучения.
Запросы идут в json(пример):
```json
{
    "version": "1.0",
    "event_type": "toxic_or_not",
    "event_date": "2022-09-17T18:40:35+03:00",
    "comment":" увы увы это нужно придумать сверхъестественный сила это нужно минимум знать сила сверхъестественный вон африка верить сделать вышка пальма посадить человек наушник кокос несомненно прилететь великий дух сбросить небо парашют груз консервы белый это работать значит получиться сила характерный вполне реальный называться ввс сша отношение культ карго вполне мистический ритуализировать"
}
```
ответ так же приходит в json:
```json
{
    "body": {
        "answer": "not toxic",
        "probability": 0.985111599623384
    },
    "event_date": "2022-09-17T18:40:35+03:00",
    "event_type": "toxic_or_not",
    "version": "1.0"
}
```
где поле `answer` - ответ модели(токсичный/не токсичный текст) и `probability` - "степень уверенности" модели
