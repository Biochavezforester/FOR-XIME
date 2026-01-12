import pandas as pd
import os

# Create examples directory
os.makedirs('examples', exist_ok=True)

# ==========================================
# EJEMPLO 1: Formato MAMIFEROS (Para Estadísticos)
# ==========================================
data_mamiferos = {
    'Especie': ['Jaguar', 'Puma', 'Ocelote', 'Tapir', 'Pecarí', 'Venado'],
    'Sitio_1': [5, 3, 8, 2, 12, 7],
    'Sitio_2': [3, 4, 6, 1, 10, 5],
    'Sitio_3': [7, 2, 5, 3, 15, 9],
    'Sitio_4': [4, 5, 7, 2, 8, 6],
    'EVENTO INDEPENDIENTE': [19, 14, 26, 8, 45, 27]
}

df_mamiferos = pd.DataFrame(data_mamiferos)

# Guardar como Excel
with pd.ExcelWriter('examples/ejemplo_mamiferos.xlsx', engine='openpyxl') as writer:
    df_mamiferos.to_excel(writer, sheet_name='Datos', index=False)

print("Creado: examples/ejemplo_mamiferos.xlsx")

# ==========================================
# EJEMPLO 2: Formato EVENTOS (Para Generar Eventos Independientes)
# ==========================================
data_eventos = {
    'sitio': [1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 1, 2],
    'especie': ['JAGUAR', 'PUMA', 'OCELOTE', 'JAGUAR', 'JAGUAR', 'PUMA', 'TAPIR', 
                'JAGUAR', 'OCELOTE', 'VENADO', 'PUMA', 'PUMA', 'JAGUAR'],
    'eventos_independientes': [5, 3, 8, 6, 3, 4, 1, 7, 5, 9, 2, 4, 2]
}

df_eventos = pd.DataFrame(data_eventos)

# Guardar como Excel
with pd.ExcelWriter('examples/ejemplo_eventos.xlsx', engine='openpyxl') as writer:
    df_eventos.to_excel(writer, sheet_name='Datos', index=False)

print("Creado: examples/ejemplo_eventos.xlsx")

print("\nArchivos de ejemplo creados exitosamente en la carpeta 'examples/'")
