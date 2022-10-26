# hack_itmo


<h2>Модель</h2>

Данные:
- https://www.kaggle.com/datasets/blackmoon/russian-language-toxic-comments.
- https://www.kaggle.com/datasets/nigula/russianinappropriatemessages?select=train.csv

В данных есть перекос классов в связи с чем взята метрика `F1`.

Процесс обучения:
1. Предобработка текста (удаление лишних символов, стоп-слов, приведение к нормальной форме - pymorphy2)
2. ООбучение с CatBoost(2500 эпох на GPU). `F1 = 84%` - для первого набора данных, `F1 = 74%` - для второго набора данных

После скачивания репы нужно в ней же создать директории `data/russian_toxic` (для первого набора данных) и `data/russian_inappropriate_messages` - там должны быть размещены данные для обучения.

Модели: https://drive.google.com/drive/folders/16Z9H9NdqI1e-4j2clbs5U5jjyrBWQMOM?usp=sharing 

<h2>API</h2>
API создана при помощи Flask и имеет один endpoint `/predict`

Пример реквеста:
```json
{
    "event_type": "toxic_or_not",
    "comment":" увы увы это нужно придумать сверхъестественный сила это нужно минимум знать сила сверхъестественный вон африка верить сделать вышка пальма посадить человек наушник кокос несомненно прилететь великий дух сбросить небо парашют груз консервы белый это работать значит получиться сила характерный вполне реальный называться ввс сша отношение культ карго вполне мистический ритуализировать"
}
```


Пример респонса:
```json
{
    "body": {
        "answer": "not toxic",
        "probability": 0.985111599623384
    }
}
```
где поле `answer` - ответ модели(токсичный/не токсичный текст) и `probability` - "степень уверенности" модели


<h2>Deploy</h2>
Проект описан двумя сервисами: `api` и `bot`, каждый из них запускается отдельно в докере, а вся система целиком поднимается через `docker-compose`:

```
> docker-compose up

CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS                                       NAMES
e3799fe52a16   api       "sh -c 'python3 __ma…"   7 minutes ago   Up 7 minutes   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   hackitmo_api_1
c3717b7a1257   tg_bot    "sh -c 'python3 __ma…"   7 minutes ago   Up 7 minutes                                               hackitmo_tg_bot_1

```

<h2>Общая архитектура</h2>

![Blank diagram-2](https://user-images.githubusercontent.com/48191103/194870985-e313bed2-5dc2-4d5c-b9d2-e3a4467f5790.png)

