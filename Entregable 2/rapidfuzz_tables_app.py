import os
import pandas as pd
from rapidfuzz_table_app_2 import execute_dynamic_matching
import mysql.connector

CARPETA_DESTINO = "C:/Users/Lenovo/Desktop/mi_proyecto_git/Entregable 2/Archivos"  
os.makedirs(CARPETA_DESTINO, exist_ok=True)

def mostrar_resultados(resultados):
    opcion = input('¿Cómo deseas ver los resultados? (DataFrame/List): ').strip().lower()
    if opcion == 'dataframe':
        df = pd.DataFrame(resultados)
        print(df)
        return df
    elif opcion == 'list':
        print(resultados)
        return resultados
    else:
        print("Opcion no valida, por favor, escriba exactamente alguna de las opciones dadas en pantalla")
        print(resultados)
        return resultados

def exportar_a_csv(resultados, nombre_archivo="resultados.csv", columnas=None, renombres=None):
    if not resultados:
        print("No se puede exportar: la lista de resultados está vacía.")
        return
    ruta_completa = os.path.join(CARPETA_DESTINO, nombre_archivo)
    df = pd.DataFrame(resultados)
    if columnas:
        if 'score' not in columnas:
            columnas = ['score'] + [col for col in columnas if col != 'score']
        df = df[columnas]
        if renombres:
            df = df.rename(columns=renombres)
    df.to_csv(ruta_completa, index=False)
    print(f"Resultados exportados a {ruta_completa}")

def exportar_a_xlsx(resultados, nombre_archivo="resultados.xlsx", columnas=None, renombres=None):
    if not resultados:
        print("No se puede exportar: la lista de resultados está vacía.")
        return
    ruta_completa = os.path.join(CARPETA_DESTINO, nombre_archivo)
    df = pd.DataFrame(resultados)
    if columnas:
        if 'score' not in columnas:
            columnas = ['score'] + [col for col in columnas if col != 'score']
        df = df[columnas]
        if renombres:
            df = df.rename(columns=renombres)
    df.to_excel(ruta_completa, index=False)
    print(f"Resultados exportados a {ruta_completa}")

def separar_coincididos(resultados, umbral=97):
    coincididos = []
    no_coincididos = []
    for r in resultados:
        score_str = str(r.get('score', '0')).replace('%', '')
        try:
            score_val = float(score_str)
        except ValueError:
            score_val = 0
        if score_val >= umbral:
            coincididos.append(r)
        else:
            no_coincididos.append(r)
    return coincididos, no_coincididos

def crear_tabla_desde_csv(connection, table_name, csv_file):
    """
    Borra la tabla si existe y la vuelve a crear con columnas basadas en el archivo CSV.
    Todas las columnas se crean como VARCHAR(255) por simplicidad.
    """
    cursor = connection.cursor()
    try:
        df = pd.read_csv(csv_file)
        columnas = df.columns.tolist()

        # Eliminar la tabla si ya existe
        drop_query = f"DROP TABLE IF EXISTS `{table_name}`;"
        cursor.execute(drop_query)

        # Crear tabla nueva
        columnas_sql = ", ".join([f"`{col}` VARCHAR(255)" for col in columnas])
        create_query = f"CREATE TABLE `{table_name}` ({columnas_sql});"
        cursor.execute(create_query)
        connection.commit()

        print(f"Tabla '{table_name}' recreada correctamente.")
        return columnas
    except Exception as e:
        print(f"Error al crear la tabla: {e}")
        return []
    finally:
        cursor.close()

def insert_from_csv(connection, table, columns, csv_file):
    """
    Inserta datos desde un archivo CSV en la tabla indicada usando un Stored Procedure.
    """
    cursor = connection.cursor()
    try:
        df = pd.read_csv(csv_file)
        for _, row in df.iterrows():
            # Convertir valores a formato SQL ('valor1','valor2',...)
            values = []
            for col in columns:
                val = row[col]
                if pd.isna(val):
                    values.append("NULL")
                else:
                    values.append(f"'{str(val)}'")
            values_str = ",".join(values)

            # Llamar al SP
            cursor.callproc(
                "sp_insert_csv_table_001",
                (table, ",".join(columns), values_str)
            )

        connection.commit()
        print(f"Se insertaron {len(df)} filas en la tabla '{table}' usando SP.")
    except Exception as error:
        print(f"Error al insertar datos: {error}")
    finally:
        cursor.close()

params_dict = {
    "server": "localhost",
    "port": 3306,
    "username": "root",
    "password": "",
    "sourceDatabase": "crm",           
    "sourceTable": "Clientes",         
    "destDatabase": "dbo",            
    "destTable": "Usuarios",           
    "src_dest_mappings": {
        "nombre": "first_name",       
        "apellido": "last_name",      
        "email": "email"              
    }
}

resultados = execute_dynamic_matching(params_dict, score_cutoff=70)
matches_filtrados = [r for r in resultados if r.get('score', 0)]

for r in matches_filtrados:
    if 'score' in r:
        r['score'] = f"{round(float(r['score']), 2)}%"
    nombre = r.get('nombre', '')
    apellido = r.get('apellido', '')
    if nombre or apellido:
        r['nombre_completo'] = f"{nombre} {apellido}".strip()
    else:
        r['nombre_completo'] = ''

coincididos, no_coincididos = separar_coincididos(matches_filtrados, umbral=97)
print(f"Resultados mayor a 97% coincididos: {len(coincididos)}")
print(f"Resultados menores a 97% no coincididos: {len(no_coincididos)}")

mostrar_resultados(matches_filtrados)

limite = input("Cuantas filas quieres exportar? (Especifica con un numero)").strip()
if limite.isdigit():
    limite_filas = int(limite)
    if limite_filas == 0:
        print("Por favor, ingresa un numero mayor a 0. El programa se cerrará.")
        matches_filtrados = []
        exit()  
    else:
        matches_filtrados = matches_filtrados[:limite_filas]
elif limite == "" or limite == "0":
    print("Opcion no disponible, por favor asegurese de ingresar un numero mayor o igual a uno.")
    matches_filtrados = []
    exit()  

grupo_exportar = input("¿Qué resultados deseas exportar? Escribe coincididos para los que tienen score >= 97%, no_coincididos para el resto, o presiona Enter para todos: ").strip().lower()
if grupo_exportar == "coincididos":
    resultados_a_exportar = coincididos
elif grupo_exportar == "no_coincididos":
    resultados_a_exportar = no_coincididos
else:
    resultados_a_exportar = matches_filtrados

if resultados_a_exportar:
    columnas_disponibles = [col for col in resultados_a_exportar[0].keys() if col != 'score']
    print("Columnas disponibles para exportar (además de 'score' que siempre se incluye):")
    print(", ".join(columnas_disponibles))
    print("Puedes renombrar columnas usando el formato columna:nuevo_nombre (Ejemplo: nombre:Nombre,apellido:Apellido)")
    columnas_seleccionadas = input("Escribe las columnas que quieres exportar, separadas por coma (además de 'score'): ").strip()
    if not columnas_seleccionadas:
        print("Debes seleccionar al menos una columna además de 'score'. El programa se cerrará.")
        exit()
    columnas = []
    renombres = {}
    for item in columnas_seleccionadas.split(","):
        item = item.strip()
        if not item:
            continue
        if ":" in item:
            original, nuevo = item.split(":", 1)
            original = original.strip()
            nuevo = nuevo.strip()
            if original in columnas_disponibles and nuevo:
                columnas.append(original)
                renombres[original] = nuevo
        else:
            if item in columnas_disponibles:
                columnas.append(item)
    if not columnas:
        print("No se seleccionó ninguna columna válida. No se puede exportar solo la columna 'score'. El programa se cerrará.")
        exit()
    columnas = ['score'] + [col for col in columnas if col != 'score']
else:
    columnas = []
    renombres = {}

exportar = input("Deseas exportar los resultados a un archivo CSV? (Si/No): ")
if exportar.lower() == 'si':
    nombre_archivo = input("Ingresa el nombre del archivo CSV: ")
    if not nombre_archivo:
        nombre_archivo = "resultados.csv"
    elif not nombre_archivo.lower().endswith('.csv'):
        nombre_archivo += ".csv"
    exportar_a_csv(resultados_a_exportar, nombre_archivo, columnas, renombres)

exportar_xlsx = input("¿Deseas exportar los resultados a un archivo XLSX? (Si/No): ")
if exportar_xlsx.lower() == 'si':
    if not resultados_a_exportar:
        print("No hay resultados para exportar a XLSX.")
    else:
        nombre_archivo_xlsx = input("Ingresa el nombre del archivo XLSX: ")
        if not nombre_archivo_xlsx:
            nombre_archivo_xlsx = "resultados.xlsx"
        elif not nombre_archivo_xlsx.lower().endswith('.xlsx'):
            nombre_archivo_xlsx += ".xlsx"
        exportar_a_xlsx(resultados_a_exportar, nombre_archivo_xlsx, columnas, renombres)

importar = input("¿Deseas importar datos desde un archivo CSV e insertarlos en una tabla MySQL? (Si/No): ").strip().lower()
if importar == 'si':
    ruta_csv = input("Ingresa la ruta del archivo CSV a importar: ").strip()
    nombre_tabla = input("Ingresa el nombre de la tabla destino en MySQL (se recreará cada vez): ").strip()

    try:
        conexion = mysql.connector.connect(
            host=params_dict["server"],
            user=params_dict["username"],
            password=params_dict["password"],
            database=params_dict["sourceDatabase"],
            port=params_dict["port"]
        )

        columnas_tabla = crear_tabla_desde_csv(conexion, nombre_tabla, ruta_csv)

        if columnas_tabla:
            insert_from_csv(conexion, nombre_tabla, columnas_tabla, ruta_csv)

        conexion.close()
    except Exception as e:
        print(f"Error al conectar o insertar en MySQL: {e}")
