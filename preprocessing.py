import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Leer el archivo CSV
data = pd.read_csv('csv/info_para_kmeans.csv')

# Definir el rango para longitud y latitud
#Punto superior izquierdo: (29.194065, -111.101352)
#Punto inferior derecho: (28.984114, -110.867698)
longitud_range = (28.984114, 29.194065)
latitud_range = (-111.101352, -110.867698)

# Contar el total de registros antes de filtrar
total_registros = len(data)

# Filtrar los datos antes de normalizar
filtered_data = data[
    (data['longitud'] >= longitud_range[0]) & (data['longitud'] <= longitud_range[1]) &
    (data['latitud'] >= latitud_range[0]) & (data['latitud'] <= latitud_range[1])
]

# Obtener los registros excluidos
excluded_data = data[
    (data['longitud'] < longitud_range[0]) | (data['longitud'] > longitud_range[1]) |
    (data['latitud'] < latitud_range[0]) | (data['latitud'] > latitud_range[1])
]

# Contar el número de registros incluidos y excluidos
registros_incluidos = len(filtered_data)
registros_excluidos = len(excluded_data)

print(f"Registros incluidos: {registros_incluidos}")
print(f"Registros excluidos: {registros_excluidos}")

# Guardar los registros excluidos en un archivo CSV
excluded_data.to_csv('csv/colonias_excluidas.csv', index=False)

# Seleccionar las columnas numéricas para normalizar
numeric_columns = ['longitud', 'latitud', 'poblacion']

# Crear un objeto MinMaxScaler
scaler = MinMaxScaler()

# Normalizar los datos numéricos
filtered_data.loc[:, numeric_columns] = scaler.fit_transform(filtered_data[numeric_columns])

# Guardar el DataFrame normalizado en un nuevo archivo CSV
filtered_data.to_csv('csv/colonias_normalizadas_filtradas.csv', index=False)

print("Archivo CSV con datos filtrados y normalizados generado con éxito.")
print("Archivo CSV con datos excluidos generado con éxito.")
