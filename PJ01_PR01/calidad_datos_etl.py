#%% TODO librerías
from cryptography.fernet import Fernet
import pandas as pd
import glob
from DataComp.utils import get_json_file, get_file_key
from DataComp.utils import to_landing_layer, to_curated_layer, to_functional_layer

#%% TODO Lectura de variables y credenciales
var_path = r'C:\PROYECTOS\MEF\SCRIPT\DGPMI_CALIDAD_DATOS\variables.json'

var = get_json_file(var_path)

cred_path = var['credential_path'] + '\credenciales.json'
landing_path = var['landing_path']

creds = get_json_file(cred_path)

datasource_sql_files = glob.glob(var['datasource_path'] + '\*.sql')
curated_sql_files = glob.glob(var['curated_path'] + '\*.sql')
curated_rule_sql_files = glob.glob(var['curated_path'] + '\\rules\*.sql')
kpi_sql_files = glob.glob(var['kpi_path'] + '\*.sql')

#%%TODO Lectura de llave
key_file_path = var['key_path'] + '\\'+ 'filekey.key'
key = get_file_key(key_file_path)
#%%TODO esquema y ambiente
schema_ds = 'odi'
schema_dl = 'psql'
level = 'dev'

cred_ds_name = 'engine_sch_' + schema_ds + '_' + level
cred_dl_name = 'engine_sch_' + schema_dl + '_' + level
cred_dl_psycopg_name = 'engine_sch_psycopg' + '_' + level

fernet = Fernet(key)
conn_ds = fernet.decrypt(bytes(creds[cred_ds_name], 'utf-8')).decode('utf-8')
conn_dl = fernet.decrypt(bytes(creds[cred_dl_name], 'utf-8')).decode('utf-8')
conn_dl_psycopg = fernet.decrypt(bytes(creds[cred_dl_psycopg_name], 'utf-8')).decode('utf-8')

#%% TODO LANDING LAYER
datasources_df_path = var['datasource_path'] + '\datasources.csv'
df_datasources = pd.read_csv(datasources_df_path)

to_landing_layer(datasource_sql_files, df_datasources, conn_ds, landing_path, conn_dl)
#%% TODO CURATED LAYER
correct_datatypes_file = var['curated_path'] + '\\' + 'corect_data_types.csv'
df_correct_datatypes = pd.read_csv(correct_datatypes_file)
#%%
to_curated_layer(curated_rule_sql_files, df_correct_datatypes, conn_ds, conn_dl)

#%% TODO FUNCTIONAL LAYER
to_functional_layer(kpi_sql_files, conn_dl)
#%% TODO SEMANTIC LAYER
