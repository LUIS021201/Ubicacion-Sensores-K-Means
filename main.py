import generar_archivo_csv
import k_means
import map_generator

if __name__ == "__main__":
    #Extraer la información de los archivos GeoJSON y guardarla en un archivo CSV para k-means
    generar_archivo_csv.main()
    #Preprocesar los datos y aplicar el algoritmo k-means
    k_means.main()
    #Generar los mapas con los clusters y colonias
    map_generator.main()