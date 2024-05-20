import json
import geopandas as gpd
import pandas as pd
import numpy as np
import os

archivo_geojson = 'geojson_agebs_de_sonora.json'
geoframe = gpd.read_file(archivo_geojson, driver="GeoJSON", crs="EPSG:4326")
geoframe.head()

geoframe.to_crs('+proj=cea').centroid.to_crs(geoframe.crs)

geoframe['centroide'] = geoframe.geometry.centroid
print(geoframe.head())

print(geoframe.crs)

hermosillo = geoframe[geoframe['municipio'] == 'Hermosillo']
print(hermosillo.head())


archivo_geojson = "geojson_colonias_de_hermosillo.json"

geoframe_colonias = gpd.read_file(archivo_geojson, driver="GeoJSON", crs="EPSG:4326")
print("GEOFRAME CENTROID")
print(geoframe.centroid)
geoframe_colonias['centroid'] = geoframe_colonias.to_crs('+proj=cea').centroid.to_crs(geoframe_colonias.crs)
centroids = geoframe_colonias[['centroid', 'poblacion']].copy()
info_para_kmeans = geoframe_colonias[['nombre', 'centroid', 'poblacion']].copy()
print("INFO PARA K-MEANS")
print(info_para_kmeans.head())

info_para_kmeans['longitud'] = info_para_kmeans['centroid'].y
info_para_kmeans['latitud'] = info_para_kmeans['centroid'].x

# Añadir una columna 'id'
info_para_kmeans['id'] = range(1, len(info_para_kmeans) + 1)

# Seleccionar y reordenar las columnas
info_para_kmeans_csv = info_para_kmeans[['id', 'nombre', 'longitud', 'latitud', 'poblacion']]

# Guardar el DataFrame en un archivo CSV
info_para_kmeans_csv.to_csv('info_para_kmeans.csv', index=False)
geoframe_colonias.drop(['centroid'], axis=1, inplace=True)

print(centroids)


print(geoframe_colonias.head())


print("FIN")
