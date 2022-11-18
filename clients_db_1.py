import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
            create table if not exists clients(
                clients_id serial primary key,
                name varchar (40) unique,
                surname varchar (40) unique,
                email varchar (40) unique
            );
            
            create table if not exists fons(
                clients_id serial primary key,
                id_phones integer,
                foreign key (id_phones) REFERENCES clients(clients_id) on delete cascade,
                phone varchar unique
                );
            ''')
    conn.commit()

def add_client(conn, name: str, surname: str, email: str, phone=None):
    with conn.cursor() as cur:
    
        cur.execute('''insert into clients (name, surname, email) 
            values (%s, %s, %s) 
            returning clients_id, name, surname, email;''', (name, surname, email))
        id_phones = cur.fetchone()[0]
        print (cur.fetchone())
        print ('id клиента: ', id_phones)
        cur.execute ('''insert into fons (id_phones, phone) 
            values (%s, %s) returning phone;''', (id_phones, phone))
        print (cur.fetchone())
        
def data_clients(conn):
    name = input('Введите имя клиента: ')
    surname = input('Введите фамилию клиента: ')
    email = input('Введите email клиента (англ.): ')
    phone = input('Введите номер телефона клиента (без скобок и пробелов): ')
    add_client(conn, name, surname, email, phone)

def add_phone(conn, id_phones, phone_n, phone):
    with conn.cursor() as cur:
        
        if phone_n == 1:
            cur.execute ('''insert into fons (id_phones, phone) 
                values (%s, %s) returning phone;''', (id_phones, phone))
        else:
            cur.execute ('''insert into fons (id_phones, phone_2) 
                values (%s, %s) returning phone;''', (id_phones, phone))

def change_client(conn, clients_id, name=None, surname=None, email=None, phone=None):
    print (clients_id, name, surname, email, phone)
    with conn.cursor() as cur:
        if name != '':
            cur.execute (''' 
            update clients set name = %s where clients_id = %s;''', (name, clients_id))
        
        if surname != '':
            cur.execute (''' 
            update clients set surname = %s where clients_id = %s;''', (surname, clients_id))
        
        if email != '':
            cur.execute (''' 
            update clients set email = %s where clients_id = %s;''', (email, clients_id))
        
        if phone != '':
            cur.execute (''' 
            update fons set phone = %s where clients_id = %s;''', (phone, clients_id))

def delete_phone(conn, clients_id):
    with conn.cursor() as cur:
        cur.execute('''
        delete from fons
        where clients_id = %s;''', (clients_id,))

def delete_client(conn, clients_id):
    with conn.cursor() as cur:
        cur.execute('''
        delete from clients
        where clients_id = %s;''', (clients_id,))

def find_client(conn, name=None, surname=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute('''
        select * from clients
        left join fons on clients.clients_id = fons.id_phones
        where  name = %s or surname = %s or email = %s or phone = %s;''', (name, surname, email, phone))
        print(cur.fetchone())
        

with psycopg2.connect(database="clients_db", user="postgres", password="Mikmik38") as conn:
    
    create_db(conn)
    
    add_cl = input('Are you want to add new client?(y/n): ')
    if add_cl == 'y':
        data_clients(conn)

    find_cl = input('Найти клиента? (y/n): ')
    if find_cl == 'y':
        name = input('name: ')
        surname = input('surname: ')
        email = input('email: ')
        phone = input('phone: ')
        find_client(conn, name, surname, email, phone)

    add_ph = input('Are you want to add new clients phone?(y/n): ')
    if add_ph == 'y':
        clients_id = input('Введите id клиента: ')
        phone_nn = input('Телефон считается основным? (y/n): ')
        if phone_nn == 'y':
            phone_n = 1
        else:
            phone_n = 2
        phone = input('Введите номер телефона клиента: ')
        add_phone(conn, clients_id, phone_n, phone)
    
    del_f = input('Удалить телефон клиента? (y/n): ')
    if del_f == 'y':
        clients_id = input('id = ')
        delete_phone(conn, clients_id)

    change_date = input('Изменить данные клиента? (y/n): ')
    if change_date == 'y':
        clients_id = input('clients_id: ')
        name = input('name: ')
        surname = input('surname: ')
        email = input('email: ')
        phone = input('phone: ')
        change_client(conn, clients_id, name, surname, email, phone)

    del_cl = input('Удалить клиента? (y/n): ')
    if del_cl == 'y':
        clients_id = input('clients_id = ')
        delete_client(conn, clients_id)
    
   

conn.close()