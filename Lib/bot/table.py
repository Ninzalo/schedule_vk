import sqlite3
from config import db_path


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
    user_id        INTEGER  UNIQUE
                            NOT NULL,
    date           DATETIME NOT NULL
                            DEFAULT ( (DATETIME('now') ) ),
    on_stage       STRING   NOT NULL
                            DEFAULT ('home'),
    mode           STRING   NOT NULL
                            DEFAULT ('night'),
    quality        INTEGER  NOT NULL
                            DEFAULT (1),
    chosen_preset  INTEGER  NOT NULL
                            DEFAULT (1),
    new_group      INTEGER  DEFAULT (0),
    on_delete_page INTEGER  DEFAULT (0) 
); """
    cur.execute(sql)
    conn.commit()


def create_tables() -> None:
    _users_table()
    _passwords_table()
    _users_info_table()
