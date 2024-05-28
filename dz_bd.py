import psycopg2

# Создание таблиц
def create_db(conn):
    cur.execute("""
                CREATE TABLE IF NOT EXISTS clients(
                   id SERIAL PRIMARY KEY,
                   name VARCHAR(40) NOT NULL,
                   surename VARCHAR(40) NOT NULL,
                   email VARCHAR(80) UNIQUE NOT NULL
                   )
               """)
    cur.execute("""
               CREATE TABLE IF NOT EXISTS tel_clients(
                    client_id integer not null references clients(id),
                    tel VARCHAR(216)
                    )
               """)
    pass
# Добавление клиента
def add_client(conn, name, surename, email, tel=None) -> int:
    cur.execute("""
        INSERT INTO clients(name, surename, email)
        VALUES(%s, %s, %s)
        RETURNING id, name, surename, email;
        """, (name, surename, email))
    client_id = cur.fetchone()[0]
    cur.execute("""
        INSERT INTO tel_clients(client_id, tel)
        VALUES(%s, %s)
        RETURNING client_id, tel;
        """, (client_id, tel))
    pass

# Поиск телефонных номеров (вспомогательная функция)
def find_tel(conn, id) -> int:
    cur.execute("""
    SELECT tel from tel_clients
    WHERE client_id = %s;
    """,(id))
    tels_client = [i[0] for i in cur.fetchall()]
    print(tels_client)
    return tels_client

# Добавить телефонный номер
def add_tel(conn,id, tel) -> int:
    client_id = id
    tel_client = find_tel(conn,id)
    print(tel_client)
    if None in tel_client:
        cur.execute("""
        UPDATE tel_clients
            SET tel = %s
            WHERE client_id = %s
        """, (tel, client_id))
        print('Номер телефона успешно добавлен клиенту')
    else:
        if tel in tel_client:
            print('Указанный номер телефона уже зарегистрирован в БД у данного клинта')
        else:
            cur.execute("""
            INSERT INTO tel_clients(client_id, tel)
            VALUES(%s,%s)
            RETURNING client_id, tel;
            """,(client_id, tel))
            print('Клиенту добавлен дополнительный номер')
    pass

#Редактирование/изменение данных клиента
def edit_client(conn, id, name=None, surename=None, email=None, tel_new=None, tel_old=None) -> int:
    if name == None:
        pass
    else:
        cur.execute("""
        UPDATE clients
        SET name = %s
        WHERE id = %s;
        """, (name, id))
    if surename == None:
        pass
    else:
        cur.execute("""
        UPDATE clients
        SET surename = %s
        WHERE id = %s;
        """, (surename, id))
    if email == None:
        pass
    else:
        cur.execute("""
        UPDATE clients
        SET email = %s
        WHERE id = %s;
        """, (email, id))
    if tel_old == None:
        pass
    else:
        if tel_old not in find_tel(conn,id):
            print('Изменяемый номер отсутствует у клиента')
        else:
            if tel_new == None:
                print('Не указан номер телефона для замены')
            else:
                print(find_tel(conn,id))
                if tel_new in find_tel(conn,id):
                    print('Добавляемый номер уже зарегистрирован у клиента')
                else:
                    cur.execute("""
                    UPDATE tel_clients
                    SET tel = %s
                    WHERE client_id = %s AND tel = %s;
                    """, (tel_new, id, tel_old))

# Удаление телефонного номера
def del_tel(conn,id, tel) -> int:
    client_id = id
    tel_client = find_tel(conn,id)
    if tel in tel_client:
        cur.execute("""
        DELETE from tel_clients
        WHERE client_id = %s AND tel =%s
        """, (client_id, tel))
    else:
        print('Удаляемый номер отсутствует у клиента')

# Удаление клиента
def del_client(conn,id) -> int:
    cur.execute("""
    SELECT id from clients
    """)
    id_client = [i[0] for i in cur.fetchall()]
    # client_id = id
    if int(id) in id_client:
        cur.execute("""
        DELETE from tel_clients
        WHERE client_id = %s
        """,(id,))
        cur.execute("""
        DELETE from clients
        WHERE id = %s
        """,(id,))
    else:
        print('Клиент отсутствует в БД')

# Поиск клиента
def find_client(conn, name=None, surename=None, email=None, tel=None) -> int:
    temp = []
    if name == None:
        list_name = []
        pass
    else:
        cur.execute("""
        SELECT id FROM clients c
        JOIN tel_clients tc ON c.id = tc.client_id
        WHERE name = %s;
        """, (name,))
        list_name = [i[0] for i in cur.fetchall()]
    temp += list_name
    if surename == None:
        list_surename = []
        pass
    else:
        cur.execute("""
            SELECT id FROM clients c
            JOIN tel_clients tc ON c.id = tc.client_id    
            WHERE surename = %s;
            """, (surename,))
        list_surename = [i[0] for i in cur.fetchall()]
    temp += list_surename
    if email == None:
        list_email = []
        pass
    else:
        cur.execute("""
            SELECT id FROM clients c
            JOIN tel_clients tc ON c.id = tc.client_id
            WHERE email = %s;
            """, (email,))
        list_email = [i[0] for i in cur.fetchall()]
    temp += list_email
    if tel == None:
        list_tel = []
        pass
    else:
        cur.execute("""
            SELECT id FROM clients c
            JOIN tel_clients tc ON c.id = tc.client_id
            WHERE tel = %s;
            """, (tel,))
        list_tel = [i[0] for i in cur.fetchall()]
    temp += list_tel
    id_client = (max(set(temp), key = temp.count))
    cur.execute("""
    SELECT name, surename, email, tel FROM clients c
    JOIN tel_clients tc ON c.id = tc.client_id
    WHERE id = %s;
    """,(id_client,))
    print(cur.fetchall())
with psycopg2.connect(database='netdb',user='postgres',password='*********') as conn:
    with conn.cursor() as cur:
    # создание таблиц
        # create_db(conn)
    # создание клиентов
        # add_client(conn, 'Viktor', 'Savin', 'savind@mail.ru')
        # add_client(conn, 'Petr', 'Petrov', 'petrovp@mail.ru', '89131234567')
        # add_client(conn, 'Sergey', 'Smirnov', 'smirnovs@mail.ru')
    # добавление телефонного номера клиенту
        find_tel(conn, id='4')
    conn.commit()  # фиксируем в БД

conn.close()