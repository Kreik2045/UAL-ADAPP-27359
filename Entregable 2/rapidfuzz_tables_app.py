from rapidfuzz_table_app_2 import execute_dynamic_matching
import pandas as pd

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