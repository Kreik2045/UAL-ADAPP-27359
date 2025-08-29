import mysql.connector
import csv
from datetime import datetime
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

config_clientes = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'port': 3306,
    'database': 'crm'
}

config_usuarios = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'port': 3306,
    'database': 'dbo'
}

def insertar_clientes(cursor, reader):
    # Optimización 2: El archivo CSV se abre una sola vez y se pasa el reader a la función
    for row in reader:
        cliente_id, nombre, apellido, email, fecha_str = row
        fecha_mysql = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")
        cursor.execute("SELECT COUNT(*) FROM clientes WHERE email = %s", (email,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO clientes (cliente_id, nombre, apellido, email, FechaRegistro)
                VALUES (%s, %s, %s, %s, %s)
            """, (cliente_id, nombre, apellido, email, fecha_mysql))
        else:
            print(f"Cliente con email {email} ya existe, se omite.")

def insertar_usuarios(cursor, reader):
    # Optimización 2: El archivo CSV se abre una sola vez y se pasa el reader a la función
    for row in reader:
        userId, username, first_name, last_name, email, password_hash, rol, fecha_str = row
        fecha_mysql = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = %s OR username = %s", (email, username))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO usuarios (userId, username, first_name, last_name, email, password_hash, rol, fecha_creacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (userId, username, first_name, last_name, email, password_hash, rol, fecha_mysql))
        else:
            print(f"Usuario {username} o email {email} ya existe, se omite.")

def main():
    try:
        # Optimización 1: Uso de 'with' para manejar la conexión y el cursor automáticamente
        with mysql.connector.connect(**config_clientes) as conn_c, conn_c.cursor() as cursor_c, \
             open("clientes.csv", newline='', encoding='utf-8') as csvfile_c:
            reader_c = csv.reader(csvfile_c)
            next(reader_c)
            insertar_clientes(cursor_c, reader_c)
            conn_c.commit()
            print("Clientes insertados correctamente.")
    except mysql.connector.Error as err:
        print(f"Error clientes: {err}")

    try:
        # Optimización 1: Uso de 'with' para manejar la conexión y el cursor automáticamente
        with mysql.connector.connect(**config_usuarios) as conn_u, conn_u.cursor() as cursor_u, \
             open("usuarios.csv", newline='', encoding='utf-8') as csvfile_u:
            reader_u = csv.reader(csvfile_u)
            next(reader_u)
            insertar_usuarios(cursor_u, reader_u)
            conn_u.commit()
            print("Usuarios insertados correctamente.")
    except mysql.connector.Error as err:
        print(f"Error usuarios: {err}")

if __name__== "__main__":
    main()