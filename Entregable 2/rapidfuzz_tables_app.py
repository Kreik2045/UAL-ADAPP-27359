import os
from rapidfuzz_table_app_2 import execute_dynamic_matching
import pandas as pd

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

def exportar_a_csv(resultados, nombre_archivo="resultados.csv"):
    if not resultados:
        print("No se puede exportar: la lista de resultados está vacía.")
        return
    ruta_completa = os.path.join(CARPETA_DESTINO, nombre_archivo)
    df = pd.DataFrame(resultados)
    df.to_csv(ruta_completa, index=False)
    print(f"Resultados exportados a {ruta_completa}")

def exportar_a_xlsx(resultados, nombre_archivo="resultados.xlsx"):
    if not resultados:
        print("No se puede exportar: la lista de resultados está vacía.")
        return
    ruta_completa = os.path.join(CARPETA_DESTINO, nombre_archivo)
    df = pd.DataFrame(resultados)
    df.to_excel(ruta_completa, index=False)
    print(f"Resultados exportados a {ruta_completa}")

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
elif limite == "" or limite == "0":
    print("Opcion no disponible, por favor asegurese de ingresar un numero mayor o igual a uno")
    matches_filtrados = []
exportar = input("Deseas exportar los resultados a un archivo CSV? (Si/No): ")
if exportar.lower() == 'si':
    nombre_archivo = input("Ingresa el nombre del archivo CSV: ")
    if not nombre_archivo:
        nombre_archivo = "resultados.csv"
    elif not nombre_archivo.lower().endswith('.csv'):
        nombre_archivo += ".csv"
    exportar_a_csv(matches_filtrados, nombre_archivo)
exportar_xlsx = input("¿Deseas exportar los resultados a un archivo XLSX? (Si/No): ")
if exportar_xlsx.lower() == 'si':
    if not matches_filtrados:
        print("No hay resultados para exportar a XLSX.")
    else:
        nombre_archivo_xlsx = input("Ingresa el nombre del archivo XLSX: ")
        if not nombre_archivo_xlsx:
            nombre_archivo_xlsx = "resultados.xlsx"
        elif not nombre_archivo_xlsx.lower().endswith('.xlsx'):
            nombre_archivo_xlsx += ".xlsx"
        exportar_a_xlsx(matches_filtrados, nombre_archivo_xlsx)