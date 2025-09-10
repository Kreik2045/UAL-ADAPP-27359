
## 1. ¿Qué pasa si hay errores tipográficos en el apellido?
Ejemplo: "Perezz" vs "Perez"
Respuesta:El algoritmo devuelve un puntaje alto (≈ 90–95%) porque las cadenas son similares. Por lo tanto, esto significa que pequeños 
errores de tipeo no afectan mucho la coincidencia.

## 2. ¿Qué pasa si faltan acentos o caracteres especiales?
Ejemplo: "Pérez" vs "Perez"
Respuesta: Los acentos cuentan como diferencias de carácter. Así que el archivo RapidFuzz devuelve un puntaje ligeramente menor 
(≈ 90%) aunque para un humano es el mismo apellido.

## 3. ¿Qué pasa si dos registros tienen un puntaje muy parecido?
Ejemplo:
- "Perezz" vs "Perez" → Score = 93
- "Peres" vs "Perez" → Score = 91
Respuesta: Si ambos tienen puntajes similares, el algoritmo se da vueltas por si mismo, y no sabe cuál es el mejor.  
Una solucion que podría ser sería el:
- Dar prioridad a un campo más importante (ej. Email sobre Apellido).

## 4. ¿Qué pasa si el nombre coincide pero el correo es muy diferente?
Ejemplo:
- Nombre: "Juan Perez" vs "Juan Perez" → Score muy alto (100).
- Email: "juanperez@gmail.com" vs "luisrodriguez@yahoo.com" → Score muy bajo.

Si todas las columnas pesan igual, el nombre puede compensar el mal puntaje del email y dar un match falso.
Una solución a este problema sería: 
- Asignar mayor peso al correo electrónico, ya que es más único.

## 5. Limitaciones de tratar todas las columnas con la misma importancia
Respuesta: Aquí lo que pasa es que si por ejemplo, nombre, apellido y email pesan igual, un match en “nombre” podría 
sobrevalorarse aunque el email sea totalmente distinto.

## 6. Ejemplos de situaciones reales donde puede haber problemas
Respuesta: 
- Una base de clientes en un local o empresa, por ejemplo, Dos clientes diferentes llamados "Juan Pérez" podrían confundirse si el 
email no se toma en cuenta correctamente.
- Registros hospitalarios: Pacientes con apellidos comunes (ej. “Hernández”) podrían mezclarse si los identificadores únicos no se priorizan.
- E-commerce: Dos usuarios con el mismo nombre podrían recibir correos promocionales equivocados si no se valida bien el correo o ID de cliente.

## 7. Conclusión del análisis
- RapidFuzz y algoritmos similares son muy útiles para detectar coincidencias con errores tipográficos o de acentos, pero tienen limitaciones.
- Para usarlos en producción se recomienda:
  - Preprocesar datos (quitar acentos, normalizar mayúsculas/minúsculas).
  - Asignar pesos diferentes a columnas (ej. Email > Apellido > Nombre).
  - Establecer un umbral mínimo de similitud.
  - Usar validación manual en casos ambiguos.


