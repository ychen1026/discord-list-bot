import sqlite3


con = sqlite3.connect("lists.db")
cur = con.cursor()

try:
    cur.execute("""
        CREATE TABLE lists(
        guild_id INT,
        list_name varchar(128),
        PRIMARY KEY(guild_id, list_name)
        )
        """)
except: # ignore table already exists
    pass

try:
    cur.execute("""
        CREATE TABLE items(
        guild_id INT,
        list_name varchar(128),
        item_name varchar(128),
        FOREIGN KEY (guild_id, list_name) REFERENCES lists(guild_id, list_name)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        UNIQUE (guild_id, list_name, item_name)
        )
        """)
except: # ignore table already exists
    pass

# print(cur.execute("SELECT name FROM sqlite_master").fetchall())

async def insert_new_list(guild_id: int, list_name: str):
    try:
        cur.execute("INSERT INTO lists VALUES (?, ?)", (guild_id, list_name))
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in e.args[0]:
            return -1
    else:
        con.commit()
    return 0

async def show_all_lists(guild_id: int):
    cur.execute("SELECT list_name FROM lists WHERE guild_id = ?", (guild_id,))
    res = cur.fetchall()

    if not res == []:
        return [i[0] for i in res]
    return []

async def insert_item_to_list(guild_id: int, list_name: str, item: str):
    res = cur.execute("SELECT * FROM lists WHERE guild_id = ? AND list_name = ?", (guild_id, list_name))
    if res.fetchone() is None:
        return -1
    try:
        cur.execute("INSERT INTO items VALUES (?, ?, ?)", (guild_id, list_name, item))
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in e.args[0]:
            return -1
    else:
        con.commit()
    return 0

async def show_items_in_list(guild_id: int, list_name: str):
    cur.execute("SELECT item_name FROM items WHERE guild_id = ? AND list_name = ?", (guild_id, list_name))
    res = cur.fetchall()

    if not res == []:
        return [i[0] for i in res]
    return []

async def delete_list(guild_id: int, list_name: str):
    cur.execute("DELETE FROM lists WHERE guild_id = ? AND list_name = ?", (guild_id, list_name))


async def delete_item(guild_id: int, list_name: str, item_name: str):
    cur.execute("DELETE FROM items WHERE guild_id = ? AND list_name = ? AND item_name = ?", (guild_id, list_name, item_name))
