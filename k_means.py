import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score


def main():
    # PREPROCESAMIENTO DE LOS DATOS
    data = pd.read_csv('csv/info_para_kmeans.csv')

    # Definir el rango para longitud y latitud
    # Punto superior izquierdo: (29.194065, -111.101352)
    # Punto inferior derecho: (28.984114, -110.867698)
    longitud_range = (28.984114, 29.194065)
    latitud_range = (-111.101352, -110.867698)

    # Contar el total de registros antes de filtrar
    total_registros = len(data)

    # Nos aseguramos que las colonias no se encuentran fuera de la localidad de Hermosillo
    filtered_data = data[
        (data['longitud'] >= longitud_range[0]) & (data['longitud'] <= longitud_range[1]) &
        (data['latitud'] >= latitud_range[0]) & (data['latitud'] <= latitud_range[1])
        ]

    # Guardar los registros filtrados en un archivo CSV
    filtered_data.to_csv('csv/colonias_filtradas.csv', index=False)

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

    print("Archivo CSV con datos filtrados.")
    print("Archivo CSV con datos excluidos generado con éxito.")
    # Seleccionar las columnas numéricas para normalizar
    numeric_columns = ['longitud', 'latitud', 'poblacion']

    # Guardamos una copia de las colonias sin normalizar
    colonias_sin_normalizar = filtered_data.copy()

    # Crear un objeto MinMaxScaler
    scaler = MinMaxScaler()

    # Normalizar los datos numéricos
    filtered_data.loc[:, numeric_columns] = scaler.fit_transform(filtered_data[numeric_columns])

    scaler.fit(data[numeric_columns])  # Ajustar el scaler a los datos originales

    data_normalizada = filtered_data

    # Seleccionar las columnas para el algoritmo k-means
    features = data_normalizada[['longitud', 'latitud', 'poblacion']]

    # Definir el número de clusters
    k = 10

    # Crear el modelo k-means
    kmeans = KMeans(n_clusters=k, random_state=42)

    # Ajustar el modelo a los datos
    kmeans.fit(features)

    # Añadir las etiquetas de los clusters al DataFrame original
    data_normalizada['cluster'] = kmeans.labels_
    colonias_sin_normalizar['cluster'] = kmeans.labels_

    # Obtener los centros de los clusters normalizados
    cluster_centers_normalized = kmeans.cluster_centers_

    # Aplicar la transformación inversa a los centros de los clusters
    cluster_centers = scaler.inverse_transform(cluster_centers_normalized)

    # Convertir los centros de los clusters a un DataFrame de Pandas
    cluster_centers_df = pd.DataFrame(cluster_centers, columns=['longitud', 'latitud', 'poblacion'])

    # Agregar la columna de etiquetas a los centros de los clusters

    cluster_centers_df['cluster_id'] = range(0, k)

    # Guardar los centros de los clusters en un archivo CSV
    cluster_centers_df.to_csv('csv/clusters.csv', index=False)
    print("Archivo CSV con los clusters generado con éxito.")

    # Imprimir los centros de los clusters
    print("Centros de los clusters:")
    for i, center in enumerate(cluster_centers):
        print(f"Cluster {i}: Longitud={center[0]}, Latitud={center[1]}, Poblacion={center[2]}")

    # Guardar el DataFrame con las etiquetas de los clusters en un nuevo archivo CSV
    colonias_sin_normalizar.to_csv('csv/colonias_con_clusters.csv', index=False)
    print("Archivo CSV con los clusters asignados a las colonias generado con éxito.")

    # Evaluar el clustering
    silhouette_avg = silhouette_score(features, kmeans.labels_)
    inertia = kmeans.inertia_

    print(f"Silhouette Score: {silhouette_avg}")
    print(f"Inertia: {inertia}")


if __name__ == '__main__':
    main()
