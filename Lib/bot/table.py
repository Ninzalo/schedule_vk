import sqlite3
from config import db_path


def _users_table():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    sql = """ CREATE TABLE IF NOT EXISTS users (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT
                               UNIQUE,
    user_id            INTEGER NOT NULL,
    on_stage           STRING  DEFAULT ('home'),
    form               STRING,
    fac                STRING,
    group_page         INTEGER DEFAULT (1),
    session_group_page INTEGER DEFAULT (1),
    group_name         STRING  DEFAULT NULL,
    subgroup           STRING,
    quality            INTEGER DEFAULT (1),
    mode               STRING  DEFAULT ('night'),
    week_page          INTEGER DEFAULT (0),
    date_page          INTEGER DEFAULT (1),
    daily_mail         INTEGER DEFAULT (0),
    weekly_mail        INTEGER DEFAULT (0),
    preset_num         INTEGER NOT NULL
                               DEFAULT (1) 
); """    
    cur.execute(sql)
    conn.commit()

def _passwords_table():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    sql = """ CREATE TABLE IF NOT EXISTS passwords (
    id         INTEGER PRIMARY KEY AUTOINCREMENT
                       UNIQUE,
    user_id    INTEGER NOT NULL,
    password   STRING  NOT NULL,
    creator_id INTEGER NOT NULL,
    privacy    INTEGER
); """    
    cur.execute(sql)
    conn.commit()


def create_tables():
    _users_table()
    _passwords_table()
