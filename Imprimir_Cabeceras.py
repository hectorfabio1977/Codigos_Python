import pandas as pd
import glob

# Paso 1: Cargar los archivos mensuales con ';' como separador
archivos = glob.glob(r'c:\Hector\INFORMACION SEM\COPIA_PC\DATOS\HECTOR FABIO\ESTADISTICAS\Consolidar_Meses\Matriculas\*_*.csv')
dataframes = []

for archivo in archivos:
    df = pd.read_csv(archivo, sep=';', na_filter=False, low_memory=False)
    
    # Eliminar espacios en blanco de los nombres de las columnas
    df.columns = df.columns.str.strip()
    
    # Verificar si 'PER_ID' existe después de limpiar espacios
    if 'PER_ID' not in df.columns:
        print(f"Advertencia: El archivo {archivo} no tiene la columna 'PER_ID' incluso después de limpiar espacios.")
    else:
        dataframes.append(df)

# Paso 2: Combinar todos los DataFrames en uno solo si tienen 'PER_ID'
if dataframes:
    df_consolidado = pd.concat(dataframes, ignore_index=True)
    
    # Paso 3: Eliminar duplicados usando 'PER_ID'
    df_consolidado = df_consolidado.drop_duplicates(subset=['PER_ID'])
    
    # Paso 4: Guardar el DataFrame consolidado en un nuevo archivo CSV
    df_consolidado.to_csv("matricula_consolidada_anual.csv", sep=';', index=False)
else:
    print("Error: No se encontraron archivos con la columna 'PER_ID' después de limpiar espacios.")