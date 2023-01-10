import sqlite3

def connect():
    conn = sqlite3.connect('iot.bd')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (chat_id INTEGER PRIMARY KEY , pos text, led1 integer, led2 integer, led3 integer, led4 integer, dama integer, motor text)")
    conn.commit()
    conn.close()

def insert(chat_id, pos,led1, led2, led3, led4, dama, motor):
    conn = sqlite3.connect('iot.bd')
    cur = conn.cursor()
    cur.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?)",(chat_id,pos,led1, led2, led3, led4, dama, motor))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect('iot.bd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    row = cur.fetchall()
    conn.close()
    return row

def search(chat_id='', pos=''):
    conn = sqlite3.connect('iot.bd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE chat_id=? OR pos=?",(chat_id,pos))
    row = cur.fetchall()
    conn.close()
    return row

def delete(chat_id):
    conn = sqlite3.connect('iot.bd')
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE n=?",(chat_id,))
    conn.commit()
    conn.close()

def update(pos,chat_id,led1=None, led2=None, led3=None, led4=None, dama=None, motor=None):
    conn = sqlite3.connect('iot.bd')
    cur = conn.cursor()
    if led1 != None and led2 != None and led3 != None and led4 != None and dama == None and motor == None:
        cur.execute("UPDATE users SET pos=?,led1=?,led2=?,led3=?,led4=? WHERE chat_id=?", (pos, led1, led2, led3, led4, chat_id))
    elif dama != None :
        cur.execute("UPDATE users SET pos=?,dama=? WHERE chat_id=?", (pos, dama, chat_id))
    elif motor != None:
        cur.execute("UPDATE users SET pos=?, motor=? WHERE chat_id=?", (pos, motor, chat_id))
    else:
        cur.execute("UPDATE users SET pos=? WHERE chat_id=?", (pos, chat_id))
    conn.commit()
    conn.close()


connect()