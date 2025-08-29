Este proyecto permite la conexión la base de dato, extraer datos de esta mismas y aplicar un algoritmo para la busqueda 
y coincidsencia de los mismos dato.

Requisitos
rapidfuzz 
pyodbcos

Este es el resultado que se mostrará en la busqueda de datos junto con el mejor match que se consulte en el proyecto.
    "server": "tu_server",
    "database": "tu_database",
    "username": "tu_usuario",
    "password": "tu_contraseña",
    "sourceSchema": "dbo",
    "sourceTable": "tabla_origen",
    "destSchema": "dbo",
    "destTable": "tabla_destino",
    "src_dest_mappings": {
        "nombre": "first_name",
        "Ciudad": "City"
    }

Esto es lo que conecta a una base de datos Azure SQL utilizando pyodbc.

Parámetros:
server (str): nombre del servidor
database (str): base de datos
username (str): usuario
password (str): contraseña

Se aplican algoritmos con fuzzy matching entre un registro y una lista de posibles elecciones.

ParAmetros:
queryRecord (str)
choices (list[dict])
score_cutoff (int)

dict con la mejor coincidencia encontrada:
    {
    'match_query': str,
    'match_result': str 
    'score': int,              
    'match_result_values': dict  
    }

esta es la función principal, la cual conecta a la base de datos (SQL) y extrae datos de origen y destino, y ejecuta fuzzy matching.

Parámetros:
params_dict (dict): diccionario con credenciales, tablas y mapeos de columnas.
score_cutoff (int, opcional): puntaje mínimo de similitud para aceptar un match.

    {
    "col_origen1": valor,
    "col_origen2": valor,
    "match_query": "...",
    "match_result": "...",
    "score": 95,
    "match_result_values": {...},
    "destTable": "tabla_destino",
    "sourceTable": "tabla_origen"
    }

[
    {
        'nombre': 'Juan',
        'Ciudad': 'Madrid',
        'match_query': 'JuanMadrid',
        'match_result': 'Juan de Madrid',
        'score': 92,
        'match_result_values': {'first_name': 'Juan', 'City': 'Madrid'},
        'destTable': 'tabla_destino',
        'sourceTable': 'tabla_origen'
    },
    ...
]

Después de obtener los resultados, se aplica un filtro para mostrar únicamente aquellos cuyo score sea mayor a 70.

Ejemplo de uso en el código:
    matches_filtrados = [r for r in resultados if r.get('score', 0) > 70]
    En esta linea de codigo lo que hacemos es hacer una nueva lista con los datos de score donde tengan un score mayor a 70
    Con el for recorremos nuestro resultado para solo insertar en la nueva variable los datos con mayor a 70 en socre
    print(matches_filtrados)
    y finalmente lo imprimimos


OPTIMIZACIONES REALIZADAS EN insertMysql.py:

1. Uso de 'with' para manejar la conexión y el cursor automáticamente:
   Se implementó el contexto 'with' al abrir (funcion main)
   la conexión a la base de datos y el cursor, 
   lo que garantiza el cierre correcto de recursos y mejora la seguridad del código.

2. Apertura única del archivo CSV:
   El archivo CSV se abre una sola vez en el bloque principal (funcion main) y 
   se pasa el reader a la función de inserción (funcion insertar clientes y usuarios), evitando múltiples aperturas y mejorando la eficiencia.

Ambas optimizaciones ayudan a que el código sea más robusto, eficiente y fácil de mantener