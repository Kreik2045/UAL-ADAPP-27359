from rapidfuzz import fuzz

def mostrar_resultado(texto1, texto2):
    score = fuzz.ratio(texto1, texto2)
    print(f'"{texto1}" vs "{texto2}" → Score: {score}')

print("1 Errores tipográficos:")
mostrar_resultado("Perezz", "Perez")

print("\n2 Acentos o caracteres especiales:")
mostrar_resultado("Pérez", "Perez")

print("\n3 Puntajes similares:")
mostrar_resultado("Perezz", "Perez")
mostrar_resultado("Peres", "Perez")

print("\n4 Nombre igual, email muy diferente:")
mostrar_resultado("Juan Perez", "Juan Perez")
mostrar_resultado("juanperez@gmail.com", "luisrodriguez@yahoo.com")
