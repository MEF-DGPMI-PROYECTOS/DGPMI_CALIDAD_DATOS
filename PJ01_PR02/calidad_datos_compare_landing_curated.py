#%% TODO librerías
import glob
import time

from cryptography.fernet import Fernet
from DataComp.utils import get_json_file, get_file_key
import pandas as pd
import connectorx as cx
import sweetviz as sv
import sys
#%% TODO Lectura de variables y credenciales
var_path = r'C:\PROYECTOS\MEF\SCRIPT\DGPMI_CALIDAD_DATOS\variables.json'

var = get_json_file(var_path)

cred_path = var['credential_path'] + '\credenciales.json'

creds = get_json_file(cred_path)

profiling_compare_report_path = var['profiling_report_path_curated_vs_landing']
#%%TODO Lectura de llave
key_file_path = var['key_path'] + '\\'+ 'filekey.key'
key = get_file_key(key_file_path)

#%%
datasources_df_path = var['datasource_path'] + '\datasources.csv'
df_datasources = pd.read_csv(datasources_df_path)
#%% Filtro de las fuentes a procesar
df_datasources = df_datasources[df_datasources['status'] == 1]
#%% TODO esquema y ambiente
#schema_ds = 'odi'
schema_dl = 'psql'
level = 'dev'

#cred_ds_name = 'engine_sch_' + schema_ds + '_' + level
cred_dl_name = 'engine_sch_' + schema_dl + '_' + level
#cred_dl_psycopg_name = 'engine_sch_psycopg' + '_' + level

fernet = Fernet(key)
conn_dl = fernet.decrypt(bytes(creds[cred_dl_name], 'utf-8')).decode('utf-8')
#%%
for i, row in df_datasources.iterrows():
    try:
        print("Generando Reporte Comparativo de: ", row['data_source'].upper())
        sql_landing = "select  * from landing." + str(row['data_source'])
        sql_curated = "select  * from curated." + str(row['data_source'])

        df_landing = cx.read_sql(conn_dl, sql_landing)
        if "cod_unico" in df_landing.columns:
            df_landing.rename(columns={'cod_unico': 'codigo_unico'}, inplace=True)

        if df_landing.isna().any().any():
            print("DataFrame LANDING contains missing values.")
        else:
            print("DataFrame LANDING has no missing values.")

        df_curated = cx.read_sql(conn_dl, sql_curated)
        if df_curated.isna().any().any():
            print("DataFrame CURATED contains missing values.")
        else:
            print("DataFrame CURATED has no missing values.")

        my_report = sv.compare([df_landing, 'Landing Data'], [df_curated, 'Curated Data'], pairwise_analysis='off')
        my_report.show_html(filepath=profiling_compare_report_path + '\Landing_vs_Curated_' + row['data_source'].upper() + '.html', open_browser=False)
    except Exception as e:
        print("Error en: ", row['data_source'].upper())
        print(e.args)

print("Comparativo finalizado")
time.sleep(5)
