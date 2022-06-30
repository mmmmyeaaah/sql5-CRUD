import psycopg2

def create_table(cursor):
    cursor.execute("""
        drop table phone_number;
        drop table clients;
        """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
            name VARCHAR(60) NOT NULL,
            last_name VARCHAR(60) NOT NULL,
            email VARCHAR(60) NOT NULL);
            """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phone_number(
            id SERIAL PRIMARY KEY,
            number BIGINT NOT NULL,
            client_id INTEGER NOT NULL REFERENCES clients(id));
            """)        
    conn.commit()        
    return

def add_client(cursor, first_name, last_name, email, phones=None):
    cursor.execute("""
        INSERT INTO clients(name, last_name, email)
        VALUES(%s, %s, %s);
        """, (first_name, last_name, email))
    cursor.execute("""
        SELECT id FROM clients WHERE name=%s;
        """,(first_name,)) 

    if phones != None:
        id_ = cursor.fetchone()[0]
    
        cursor.execute("""
            INSERT INTO phone_number(number, client_id)
            VALUES(%s, %s);
            """, (phones, id_))
    conn.commit()   

def add_phone(cursor, client_id, number):
    cursor.execute("""
        INSERT INTO phone_number(number, client_id)
        VALUES(%s, %s);
        """, (number, client_id))    
    conn.commit()    

def change_client(cursor, client_id, first_name=None, last_name=None, email=None, phones=None):
    if first_name != None:
        cursor.execute("""
            UPDATE clients SET name=%s WHERE id=%s;
            """, (first_name, client_id))
    if last_name != None:
        cursor.execute("""
            UPDATE clients SET last_name=%s WHERE id=%s;
            """, (last_name, client_id))
    if email != None:
        cursor.execute("""
            UPDATE clients SET email=%s WHERE id=%s;
            """, (email, client_id))
    if phones != None:
        cursor.execute("""
            UPDATE phone_number SET number=%s WHERE client_id=%s AND number=%s;
            """, (phones, client_id, input('Введите номер, который нужно заменить: ')))
    conn.commit()

def delete_phone(cursor, client_id, phone):
    cursor.execute("""
        DELETE FROM phone_number WHERE client_id=%s AND number=%s;
        """, (client_id, phone))
    conn.commit()    

def delete_client(cursor, client_id):
    cursor.execute("""
        DELETE FROM phone_number WHERE client_id=%s;
        """, (client_id,))
    cursor.execute("""
        DELETE FROM clients WHERE id=%s;
        """, (client_id,))
    conn.commit()        

def find_client(cursor, first_name=None, last_name=None, email=None, phone=None):  
    if phone != None:
        def get_id(cursor, phone):
            cursor.execute("""
                SELECT * FROM phone_number WHERE number=%s;
                """, (phone,))
            return(cursor.fetchone()[2])
       
        cursor.execute("""
            SELECT * FROM clients WHERE id=%s;
            """, (get_id(cursor, phone),)) 
        print(cursor.fetchall())
        conn.commit()          
    
    else:
        cursor.execute("""
            SELECT * FROM clients WHERE name=%s or last_name=%s or email=%s;
            """, (first_name, last_name, email))
        print(cursor.fetchall())    
        conn.commit()     
        




with psycopg2.connect(database = input('Введите название  БД: '), user = input('Введите пользователя: '), password = input('Введите пароль: ')) as conn:
    with conn.cursor() as cur:
        create_table(cur)   
        add_client(cur, 'Viktor', 'Zverev', 'spiellberg_092@mail.ru')
        add_client(cur, 'Алёша', 'Попович', 'pop@mail.ru', 88005553535)
        add_client(cur, 'Lex', 'Luthor', 'small@gmail.com', 111)
        # add_client(cur, first_name=input('Введите имя: '), last_name=input('Введите фамиляю: '), email=input('Введите email: '))
        add_phone(cur, 3, 12345)
        change_client(cur, 1, 'Виктор')
        change_client(cur, 1, last_name='Зверев')
        change_client(cur, 2, email='pop@gmail.com')
        # change_client(cur, 3, phones=999)
        # change_client(cur, 3, first_name='Alex', last_name='Lutor')
        # delete_phone(cur, 2, 88005553535)
        # delete_client(cur, 3)
        # find_client(cur, last_name='Зверев')
        # find_client(cur, phone = 111)

conn.close         
    
  