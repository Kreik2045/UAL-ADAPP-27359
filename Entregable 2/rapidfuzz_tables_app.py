from rapidfuzz_table_app_2 import execute_dynamic_matching

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
matches_filtrados = [r for r in resultados if r.get('score', 0) > 70]  
print(matches_filtrados)