import mysql.connector
import csv
from datetime import datetime

config = {
    'user': 'root',
    'password': 'hola',
    'host': 'localhost',
    'port': 3306,
    'database': 'dbo'
}

def insertar_usuarios(cursor, archivo_csv):
    with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
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
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        insertar_usuarios(cursor, "./Entregable 2/usuarios.csv")
        conn.commit()
        print("Registros insertados correctamente.")

    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err}")
        if conn:
            conn.rollback()
    except FileNotFoundError as err:
        print(f"Archivo no encontrado: {err}")
    except Exception as err:
        print(f"Otro error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
