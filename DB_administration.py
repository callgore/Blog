import sqlite3
import numpy as np
import functools
import operator
from werkzeug.security import generate_password_hash, check_password_hash

connection = sqlite3.connect("database/data", check_same_thread=False)
cursor = connection.cursor()


def initSession(u, p):
    allUser = cursor.execute("SELECT user FROM account;").fetchall()
    try:
        n = allUser.index((u,))
        Pass = cursor.execute(f"SELECT password FROM account WHERE user = '{u}';").fetchone()
        return check_password_hash(functools.reduce(operator.add, Pass), p)
    except:
        return False


def addValuesUser(u, e, p):
    if u != "" and e != "" and p != "":
        allUser = cursor.execute("SELECT user FROM account;").fetchall()
        g = functools.reduce(operator.add, allUser)
        if f'{u}' in g:
            return False
        else:
            cursor.execute(f"""INSERT INTO account
                                                VALUES ('{u}', '{e}', '{generate_password_hash(p)}'""")
            connection.commit()
            return True
    else:
        return False


def getDiscussion():
    old = []
    for i in np.unique(cursor.execute("SELECT ID FROM discussions;").fetchall()):
        old.append(cursor.execute(f"""SELECT * FROM discussions WHERE ID = '{i}';""").fetchone())
    return old


def getAllDiscussion(n):
    all = cursor.execute(f"""SELECT * FROM discussions WHERE ID = '{n}';""").fetchall()
    return all


def getTopic(n):
    one = cursor.execute(f"""SELECT name FROM discussions WHERE ID = '{n}';""").fetchone()
    return one


def addComents(id, name, user, comment, date):
    cursor.execute(f"""INSERT INTO discussions
                                        VALUES ('{id}', '{name}', '{user}', '{comment}', '{date}')""")
    connection.commit()
