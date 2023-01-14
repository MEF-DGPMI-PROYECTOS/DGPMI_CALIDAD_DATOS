#%% TODO librerías
import glob
from cryptography.fernet import Fernet
from DataComp.utils import get_json_file,  get_file_key, to_profiling_report
#%% TODO Lectura de variables y credenciales

var_path = r'C:\PROYECTOS\MEF\SCRIPT\DGPMI_CALIDAD_DATOS\variables.json'

var = get_json_file(var_path)

cred_path = var['credential_path'] + '\credenciales.json'

creds = get_json_file(cred_path)

profiling_report_path = var['profiling_report_path']

datasource_sql_files = glob.glob(var['datasource_path'] + '\*.sql')
#%%TODO Lectura de llave
key_file_path = var['key_path'] + '\\'+ 'filekey.key'
key = get_file_key(key_file_path)

#%% TODO esquema y ambiente
schema_ds = 'odi'
schema_dl = 'psql'
level = 'dev'

cred_ds_name = 'engine_sch_' + schema_ds + '_' + level
cred_dl_name = 'engine_sch_' + schema_dl + '_' + level
cred_dl_psycopg_name = 'engine_sch_psycopg' + '_' + level

fernet = Fernet(key)
conn_ds = fernet.decrypt(bytes(creds[cred_ds_name], 'utf-8')).decode('utf-8')
#%%TODO Profiling report
to_profiling_report(datasource_sql_files, profiling_report_path, conn_ds)
#%%
