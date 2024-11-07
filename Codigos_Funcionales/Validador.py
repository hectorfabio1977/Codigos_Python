import csv
import pandas as pd

# Definir el esquema esperado
COLUMNAS_ESPERADAS = [
    'ANO_INF', 'MUN_CODIGO', 'CODIGO_DANE', 
    'DANE_ANTERIOR', 'CONS_SEDE', 
    'TIPO_DOCUMENTO', 'NRO_DOCUMENTO', 'EXP_DEPTO',
    'EXP_MUN', 'APELLIDO1', 'APELLIDO2', ' NOMBRE1',
    'NOMBRE2', 'DIRECCION_RESIDENCIA', 'TEL', 'RES_DEPTO', 
    'RES_MUN', 'ESTRATO', 'SISBEN IV', 'FECHA_NACIMIENTO', 
    'NAC_DEPTO', 'NAC_MUN', 'GENERO', 'POB_VICT_CONF_RUV', 
    ' PROVIENE_SECTOR_PRIV', 'PROVIENE_OTR_MUN', 'TIPO_DISCAPACIDAD', 
    'CAP_EXC', 'ETNIA', 'RES', 'TIPO_JORNADA', 'CARACTER', 'ESPECIALIDAD', 
    'GRADO', 'GRUPO', 'METODOLOGIA', 'MATRICULA_CONTRATADA', 'REPITENTE', 
    'NUEVO', 'FUE_RECU', 'ZON_ALU', 'CAB_FAMILIA', 'BEN_MAD_FLIA', 'BEN_VET_FP', 
    'BEN_HER_NAC', 'CODIGO_INTERNADO', 'CODIGO_VALORACION_1', 'CODIGO_VALORACION_2', 
    'NUM_CONVENIO', 'PER_ID', 'APOYO_ACADEMICO_ESPECIAL', 'SRPA', 'PAIS_ORIGEN', 'TRASTORNOS_ESPECIFICOS'
]

# Especificar tipos esperados para algunas columnas
TIPOS_ESPERADOS = {
    "ANO_INF": int, 
    "PER_ID": int
}

# Especificar campos obligatorios
CAMPOS_OBLIGATORIOS = ["ANO_INF", "CODIGO_DANE",  "PER_ID"]

def validar_csv(ruta_csv):
    errores = []
    
    try:
        # Leer datos con pandas para validaciones detalladas y con encoding utf-8
        try:
            datos = pd.read_csv(ruta_csv, encoding='utf-8',sep=';')
        except UnicodeDecodeError:
            # Si utf-8 falla, intentar con latin1
            datos = pd.read_csv(ruta_csv, encoding='latin1')

        # Validar el encabezado
        encabezado = list(datos.columns)
        if encabezado != COLUMNAS_ESPERADAS:
            errores.append("Error: El encabezado no coincide con el formato esperado.")
            return errores
        
        # Validar número de columnas
        if len(encabezado) != len(COLUMNAS_ESPERADAS):
            errores.append("Error: Número de columnas incorrecto.")
                
        # Validar columnas obligatorias y tipos de datos
        for columna, tipo in TIPOS_ESPERADOS.items():
            if columna not in datos.columns:
                errores.append(f"Error: La columna '{columna}' está ausente.")
                continue
            
            # Validar tipo de datos
            if tipo == "fecha":
                # Comprobar si el valor puede convertirse en fecha
                try:
                    datos[columna] = pd.to_datetime(datos[columna], errors='raise')
                except Exception:
                    errores.append(f"Error: La columna '{columna}' tiene valores que no son fechas.")
            else:
                if not all(isinstance(val, tipo) or pd.isnull(val) for val in datos[columna]):
                    errores.append(f"Error: La columna '{columna}' no tiene el tipo de datos correcto.")
        
        # Verificar valores faltantes en campos obligatorios
        for columna in CAMPOS_OBLIGATORIOS:
            if datos[columna].isnull().any():
                errores.append(f"Error: La columna obligatoria '{columna}' tiene valores faltantes.")
                    
    except FileNotFoundError:
        errores.append("Error: Archivo no encontrado.")
    except Exception as e:
        errores.append(f"Error inesperado: {e}")

    if errores:
        return errores
    else:
        return "El archivo está correctamente formateado."

# Uso del script con la ruta específica
ruta_csv = r"C:\Hector\INFORMACION SEM\COPIA_PC\DATOS\HECTOR FABIO\ESTADISTICAS\Consolidar_Meses\Matriculas\proc7998890_Enero.csv"
resultado = validar_csv(ruta_csv)

if isinstance(resultado, list):
    for error in resultado:
        print(error)
else:
    print(resultado)