import sqlite3
from config import db_path, show_elapsed_time


def _users_table() -> None:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    sql = """ CREATE TABLE IF NOT EXISTS users (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT
                               UNIQUE,
    user_id            INTEGER NOT NULL,
    form               STRING,
    fac                STRING,
    group_page         INTEGER DEFAULT (1),
    session_group_page INTEGER DEFAULT (1),
    group_name         STRING  DEFAULT NULL,
    subgroup           STRING,
    week_page          INTEGER DEFAULT (0),
    date_page          INTEGER DEFAULT (1),
    daily_mail         INTEGER DEFAULT (0),
    weekly_mail        INTEGER DEFAULT (0),
    preset_num         INTEGER NOT NULL
                               DEFAULT (1) 
); """
    cur.execute(sql)
    conn.commit()

def _passwords_table() -> None:
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


def _users_info_table() -> None:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    sql = """ CREATE TABLE IF NOT EXISTS users_info (
    user_id             INTEGER  UNIQUE
                                 NOT NULL,
    date                DATETIME NOT NULL
                                 DEFAULT ( (DATETIME('now') ) ),
    on_stage            STRING   NOT NULL
                                 DEFAULT ('home'),
    mode                STRING   NOT NULL
                                 DEFAULT ('night'),
    quality             INTEGER  NOT NULL
                                 DEFAULT (1),
    chosen_preset       INTEGER  NOT NULL
                                 DEFAULT (1),
    new_group           INTEGER  DEFAULT (0),
    on_delete_page      INTEGER  DEFAULT (0)
); """
    cur.execute(sql)
    conn.commit()


def _teacher_search_table() -> None:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    sql = """ CREATE TABLE IF NOT EXISTS teacher_search (
    user_id             INTEGER  UNIQUE
                                 NOT NULL,
    full_search         INTEGER  DEFAULT (0),
    requested_name      STRING,
    teacher_page        INTEGER  DEFAULT (0),
    data_page           INTEGER  DEFAULT (0)
); """
    cur.execute(sql)
    conn.commit()

def _expand_table() -> None:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sqls = [
    """ ALTER TABLE users_info 
    ADD COLUMN notifications       INTEGER  DEFAULT (1)
    """,
    ]
    for sql in sqls:
        try:
            cur.execute(sql)
        except:
            if show_elapsed_time is True:
                print('[INFO] Column already added')
            pass
    conn.commit()


def create_tables() -> None:
    _users_table()
    _passwords_table()
    _users_info_table()
    _teacher_search_table()
    _expand_table()
