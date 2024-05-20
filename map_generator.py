import folium
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler


def agregar_colonias(m, colonias, radius=0):
    # Calcular el rango de valores de población para normalizar el radio del círculo de las colonias
    min_poblacion = colonias['poblacion'].min()
    max_poblacion = colonias['poblacion'].max()
    caluclar_radio = radius == 0
    # Agregar los círculos representando las colonias al mapa
    for index, row in colonias.iterrows():
        # Calcular el radio del círculo en función del valor de población
        poblacion_normalized = (row['poblacion'] - min_poblacion) / (max_poblacion - min_poblacion)
        if caluclar_radio:
            radius = 100 + poblacion_normalized * 400

        folium.Circle(
            location=[row['longitud'], row['latitud']],
            radius=radius,
            color='green',
            fill=True,
            fill_color='green',
            fill_opacity=0.3,
            popup=row['nombre']
        ).add_to(m)


def agregar_clusters(m, clusters, radius=0):
    # Agregar los centros de los clusters al mapa

    # Calcular el rango de valores de población para normalizar el radio del círculo de los clusters
    min_poblacion = clusters['poblacion'].min()
    max_poblacion = clusters['poblacion'].max()
    caluclar_radio = radius == 0
    # Agregar los círculos representando los clusters al mapa
    for index, row in clusters.iterrows():
        # Calcular el radio del círculo en función del valor de población
        poblacion_normalized = (row['poblacion'] - min_poblacion) / (max_poblacion - min_poblacion)
        if caluclar_radio:
            radius = 100 + poblacion_normalized * 400
        folium.Circle(
            location=[row['longitud'], row['latitud']],
            radius=radius,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.9,
            popup=f"Cluster {row['cluster_id']}"
        ).add_to(m)


def agregar_lineas(m, clusters, colonias):
    # Agregar las líneas que conectan los centros de los clusters con las colonias asignadas a cada cluster
    line_colors = {
        0: 'red',
        1: 'cadetblue',
        2: 'green',
        3: 'orange',
        4: 'purple',
        5: 'yellow',
        6: 'cyan',
        7: 'magenta',
        8: 'pink',
        9: 'gray'

    }
    #para hacer mapa cluster_5.html
    #line_colors = {5: 'red'}

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


def generar_mapa_solo_clusters(clusters):
    # Crear un mapa
    m = folium.Map(location=[29.089189, -111.019501], zoom_start=10)
    agregar_clusters(m, clusters, 200)

    # Guardar el mapa como un archivo HTML
    m.save('mapas/solo_clusters.html')

    print("Mapa de solo clusters generado con éxito.")


def generar_mapa_clusters_colonias_con_tamanio(clusters, colonias):
    # Crear un mapa
    m = folium.Map(location=[29.089189, -111.019501], zoom_start=10)

    agregar_colonias(m, colonias)
    agregar_clusters(m, clusters)
    # Guardar el mapa como un archivo HTML
    m.save('mapas/clusters_colonias_con_tamanio.html')

    print("Mapa de clusters y colonias con tamaño proporcional a poblacion generado con éxito.")


def generar_mapa_clusters_colonias_con_tamanio_con_lineas(clusters, colonias):
    # Crear un mapa
    m = folium.Map(location=[29.089189, -111.019501], zoom_start=10)

    agregar_colonias(m, colonias)
    agregar_lineas(m, clusters, colonias)
    agregar_clusters(m, clusters)
    # Guardar el mapa como un archivo HTML
    m.save('mapas/clusters_colonias_con_tamanio_con_lineas.html')

    print("Mapa de clusters y colonias con tamaño proporcional a poblacion y líneas generadas con éxito.")


def main():
    # Leer el archivo CSV con los clusters
    clusters = pd.read_csv('csv/clusters.csv')

    # Leer el archivo CSV con los datos de colonias
    colonias = pd.read_csv('csv/colonias_con_clusters.csv')
    generar_mapa_solo_clusters(clusters)
    generar_mapa_clusters_colonias_con_tamanio(clusters, colonias)
    generar_mapa_clusters_colonias_con_tamanio_con_lineas(clusters, colonias)


if __name__ == "__main__":
    main()
