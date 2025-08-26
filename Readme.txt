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

