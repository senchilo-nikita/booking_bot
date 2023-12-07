from pytz import timezone
import datetime
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
import sqlalchemy as sa
# import pandas as pd
from sqlalchemy import text, insert
load_dotenv()
CONNECTION_STRING = os.getenv('CONNECTION_STRING')
engine = sa.create_engine(CONNECTION_STRING)

def create_table_for_booking():
    sql_create = """CREATE TABLE booking_table
    (
        date TIMESTAMP,
        hour INT,
        user_name VARCHAR(50),
        PRIMARY KEY (date, hour)
    );"""
    engine.execute(sql_create)

def create_new_booking(hour,user,date_now):
    # создание подключения
    try:
        sql_insert = text(f"""INSERT INTO booking_table (date, hour, user_name) 
                    VALUES (TO_TIMESTAMP('{date_now.date()}', 'YYYY-MM-DD') :: TIMESTAMP AT TIME ZONE 'Europe/Moscow', 
                    {hour}, '{user}');""")
        with engine.connect() as connection: 
            connection.execute(sql_insert)
            connection.commit()
        return f'Запись сделана. Пользователь {user} на время c {hour} до {hour+1} часов'
    except Exception as e:
        print(e)
        request = text(f"""
        SELECT * FROM booking_table
        WHERE date = TO_TIMESTAMP('{date_now.date()}', 'YYYY-MM-DD') :: TIMESTAMP AT TIME ZONE 'Europe/Moscow'
        AND hour = {hour}
        """)
        with engine.connect() as con:
            result = con.execute(request)
        for row in result:
            return f'Запись уже существует. Пользователь {row[2]} на время c {row[1]} до {row[1]+1} часов'


def create_booking_plan(date_now):
    request = text(f"""
        SELECT * FROM booking_table
        WHERE date = TO_TIMESTAMP('{date_now.date()}', 'YYYY-MM-DD') :: TIMESTAMP AT TIME ZONE 'Europe/Moscow'
        ORDER BY hour
        """)
    with engine.connect() as con:
        result = con.execute(request)
    message='|{}|{}|{}|{}\n-----------------------------------------------\n'.format('Дата','Старт','Конец','Пользователь')
    for row in result:
        name = row[2]
        if len(name) > 15:
            name = name[:15]
        else:
            name = ('{: <15}'.format(name))
        hour = row[1]
        date = row[0].strftime('%d-%m-%y')
        message += ('|{: <10}|{: <4}|{: <4}|{: <15}\n'.format(date,hour,hour+1,name))
    return message