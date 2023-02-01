#%% TODO librerías
import glob
from cryptography.fernet import Fernet
from DataComp.utils import get_json_file,  get_file_key, to_profiling_report
#%% TODO Lectura de variables y credenciales

layer = sys.argv[1]
#layer = 'curated'
layer_var = ''
report_var = ''

if layer == 'landing':
    layer_var = 'landing_profile_path'
    report_var = 'profiling_report_path_landing'

elif layer == 'curated':
    layer_var = 'curated_profile_path'
    report_var = 'profiling_report_path_curated'

var_path = r'C:\PROYECTOS\MEF\SCRIPT\DGPMI_CALIDAD_DATOS\variables.json'

var = get_json_file(var_path)

cred_path = var['credential_path'] + '\credenciales.json'

creds = get_json_file(cred_path)

profiling_report_path = var[report_var]

#%%TODO Lectura de llave
key_file_path = var['key_path'] + '\\'+ 'filekey.key'
key = get_file_key(key_file_path)

#%%
datasources_df_path = var['datasource_path'] + '\datasources.csv'
df_datasources = pd.read_csv(datasources_df_path)
#%% Filtro de las fuentes a procesar
df_datasources = df_datasources[df_datasources['status'] == 1]

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
to_profiling_report(profiling_report_path, df_datasources, layer, conn_dl)
#%%
