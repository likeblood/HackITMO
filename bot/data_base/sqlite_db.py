import sqlite3 as sq
from bot.create_bot import bot, dp, counter

def sql_start():
    global base, cur
    base = sq.connect('test_bot.db')
    cur = base.cursor()
    if base:
        print('Data base Connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS info(toxic_words TEXT)')
    base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO info VALUES (?)', tuple(data.values()))
        base.commit()

async def sql_read(message):
    #if message.from_user.id == ID:
    for ret in cur.execute('SELECT * FROM info').fetchall():
        await bot.send_message(message.from_user.id, f'Запрещенные слова: {ret[0]}\nКоличество удаленных сообщений: {counter}')

def sql_read_stop_words():
    sw = set()
    for ret in cur.execute('SELECT * FROM info').fetchall():
        sw.add(ret[0])
    return sw
