import pandas as pd
import os
from ..decorators.decorators import medir_tiempo , logit
from .scraper import obtener_datos_productos

@logit
@medir_tiempo
def obtener_paginas(base_url):
    productos = []
    page = 1
    while True:
        url = f"{base_url}_Desde_{page}"
        nuevos_productos = obtener_datos_productos(url)
        if not nuevos_productos:
            break
        productos.extend(nuevos_productos)
        page += 48
        
    return productos
@medir_tiempo
@logit
def procesar_datos(productos):
    datos_procesados = []
    for nombre, precio in productos:
        # Eliminar puntos y convertir a float
        precio = float(precio.replace(".", "").replace(",", "."))
        datos_procesados.append({"Producto": nombre, "Precio": precio})
          
    return datos_procesados

@medir_tiempo
@logit
def guardar_datos_en_archivo_csv(datos, archivo):
    """Guardamos los datos en un archivo CSV"""
    df = pd.DataFrame(datos, columns=["Producto", "Precio"])
    df.to_csv('data/raw/products.csv', index=False, encoding="utf-8")
    return df
@medir_tiempo
@logit
def estadisticas_precios(df):
    df = pd.DataFrame(datos_procesados)
    print("Basic Data Analysis:")
    print(df.describe())
    print("\nProducts with highest prices: ") # Imprimimos un encabezado para los productos con los precios mas altos
    highestPrices= df.nlargest(5,"Precio") 
    print(highestPrices) # Imprimimos los 5 productos con los precios mas altos.
    return highestPrices
   

@medir_tiempo
@logit
def save_clean_data(df,outputh_path):
    """Guardamos los datos limpios en un archivo CSV"""
    if outputh_path.endswith(".csv"):
        df.to_csv(outputh_path,index=False) # Guardamos los datos en un archivo CSV.
    elif outputh_path.endswith(".xlsx"):
        df.to_excel(outputh_path, index=False) # Guardamos los datos en un archivo Excel.
    else:
        raise ValueError("Unsupported file format") # Lanzamos un error si el formato del archivo no es compatible
    print(f"Clean data saved to {outputh_path}")
    
    

if __name__ == "__main__": # Permitimos que el script solo se ejecute en este archivo
    data_path = "data/raw/productos.csv" # Definimos la ruta del archivo de datos SIN procesar.
    outputh_path = "data/processed/cleaned_products.csv" # Definimos la ruta del archivo de datos procesados

    base_url = "https://listado.mercadolibre.com.ec/computacion-notebooks"


    # ejecutar funciones
    productos= obtener_paginas(base_url)
    datos_procesados= procesar_datos(productos)
    df= guardar_datos_en_archivo_csv(productos, "data/raw/products.csv")
    df= estadisticas_precios(df)
    os.makedirs("data/processed", exist_ok=True) # Creamos el directorio para los datos procesados si no existe
    save_clean_data(df,outputh_path) # Guardamos los datos limpios en el archivo especifico