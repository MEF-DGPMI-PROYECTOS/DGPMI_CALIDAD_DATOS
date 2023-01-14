#%%TODO Configuración de Datasources
from ruamel import yaml
import great_expectations as gx
from cryptography.fernet import Fernet
from DataComp.utils import get_json_file,  get_file_key

#%% TODO Lectura de variables y credenciales
var_path = r'C:\PROYECTOS\MEF\SCRIPT\DGPMI_CALIDAD_DATOS\variables.json'

var = get_json_file(var_path)

cred_path = var['credential_path'] + '\credenciales.json'

creds = get_json_file(cred_path)
#%%TODO Lectura de llave
key_file_path = var['key_path'] + '\\'+ 'filekey.key'
key = get_file_key(key_file_path)
#%%TODO esquema y ambiente
schema_dl = 'psql'
level = 'dev'
cred_dl_name = 'engine_sch_' + schema_dl + '_' + level
fernet = Fernet(key)

#%%
CONNECTION_STRING = fernet.decrypt(bytes(creds[cred_dl_name], 'utf-8')).decode('utf-8')

#%%
data_context: gx.DataContext = gx.get_context()
#%%TODO Obtenemos las conexiones a los datos
dc_gx_path = var['gx_data_connectors_path'] + '\data_connectors.json'
data_connectors = get_json_file(dc_gx_path)
#%%
datasource_config: dict = {
    "name": cred_dl_name,
    "class_name": "Datasource",
    "module_name": "great_expectations.datasource",
    "execution_engine": {
        "class_name": "SqlAlchemyExecutionEngine",
        "module_name": "great_expectations.execution_engine",
        "connection_string": CONNECTION_STRING,
    },
}
#%%TODO Agregamos los conectores al archivo de configuración

if list(data_connectors.keys())[0] not in datasource_config:
    datasource_config = {**datasource_config, **data_connectors}
    print("'data_connectors' have been added to datasource configuration file.")
else:
    print("'data_connectors' exists.")

#%%TODO Evaluamos el archivo de configuración
print(data_context.test_yaml_config(yaml.dump(datasource_config)))
#%%TODO Agregamos el nuevo Datasourde al Data Context
try:
    data_context: gx.DataContext = gx.get_context()
    data_context.get_datasource(datasource_config['name'])
except ValueError:
    data_context.add_datasource(**datasource_config)
    print(f"Datasource {datasource_config['name']} added")
else:
    print(f"The datasource {datasource_config['name']} already exists in your Data Context!")