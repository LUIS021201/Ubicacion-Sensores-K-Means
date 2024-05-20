import folium
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

# Leer el archivo CSV con los clusters
clusters = pd.read_csv('csv/clusters.csv')

# Leer el archivo CSV con los datos de colonias
colonias = pd.read_csv('csv/colonias_con_clusters.csv')

# Crear un mapa
m = folium.Map(location=[29.089189, -111.019501], zoom_start=10)

# Calcular el rango de valores de población para normalizar el radio del círculo
min_poblacion = colonias['poblacion'].min()
max_poblacion = colonias['poblacion'].max()
# Agregar los círculos representando las colonias al mapa
for index, row in colonias.iterrows():
    # Calcular el radio del círculo en función del valor de población
    poblacion_normalized = (row['poblacion'] - min_poblacion) / (max_poblacion - min_poblacion)
    radius = 100 + poblacion_normalized * 400  # Ajusta el factor de escala según tus preferencias

    folium.Circle(
        location=[row['longitud'], row['latitud']],
        radius=radius,  # Puedes ajustar el radio según tu preferencia
        color='green',  # Color del borde del círculo
        fill=True,
        fill_color='green',  # Color de relleno del círculo
        fill_opacity=0.3,  # Opacidad del relleno
        popup=row['nombre']
    ).add_to(m)
# Agregar los centros de los clusters al mapa

min_poblacion = clusters['poblacion'].min()
max_poblacion = clusters['poblacion'].max()

# line_colors = {
#     0: 'red',
#     1: 'cadetblue',
#     2: 'green',
#     3: 'orange',
#     4: 'purple',
#     5: 'yellow',
#     6: 'cyan',
#     7: 'magenta',
#     8: 'pink',
#     9: 'gray'
#     # Agrega más colores si tienes más de 9 clusters
# }
line_colors = {

    5: 'red',

    # Agrega más colores si tienes más de 9 clusters
}
for index_clusters, cluster in clusters.iterrows():
    for index_colonias, colonia in colonias.iterrows():
        if colonia['cluster'] == cluster['cluster_id']:
            color = line_colors.get(cluster['cluster_id'], 'black')
            folium.PolyLine(
                locations=[[cluster['longitud'], cluster['latitud']], [colonia['longitud'], colonia['latitud']],
                           [cluster['longitud'], cluster['latitud']]],
                color=color,
                weight=2.5,
                opacity=0.8
            ).add_to(m)

cluster = clusters.loc[clusters['cluster_id'] == 5].iloc[0]
for index_colonias, colonia in colonias.iterrows():

    if colonia['cluster'] == 5:
        folium.PolyLine(
            locations=[[cluster['longitud'], cluster['latitud']], [colonia['longitud'], colonia['latitud']],
                       [cluster['longitud'], cluster['latitud']]],
            color='red',
            weight=2.5,
            opacity=0.8
        ).add_to(m)

# Agregar los círculos representando los clusters al mapa
for index, row in clusters.iterrows():
    # Calcular el radio del círculo en función del valor de población
    poblacion_normalized = (row['poblacion'] - min_poblacion) / (max_poblacion - min_poblacion)
    radius = 100 + poblacion_normalized * 400  # Ajusta el factor de escala según tus preferencias
    folium.Circle(
        location=[row['longitud'], row['latitud']],
        radius=200,  # Puedes ajustar el radio según tu preferencia
        color='blue',  # Color del borde del círculo
        fill=True,
        fill_color='blue',  # Color de relleno del círculo
        fill_opacity=0.9,  # Opacidad del relleno
        popup=f"Cluster {row['cluster_id']}"
    ).add_to(m)
# Guardar el mapa como un archivo HTML
m.save('mapas/cluster_5.html')

print("Mapa generado con éxito.")
