#!
# # Create Your Checkpoint
# Use this notebook to configure a new Checkpoint and add it to your project:
#
# **Checkpoint Name**: `ckpt_{table_name}`
import time
import tqdm
from DataComp.utils import get_json_file
import pandas as pd
# In[12]:
from ruamel.yaml import YAML
import great_expectations as ge
from pprint import pprint
import sys
yaml = YAML()
context = ge.get_context()

# In[2]:
layer = sys.argv[1]
layer_var = ''
#table_name = sys.argv[2]

if layer == 'landing':
    layer_var = 'lnd'
elif layer == 'curated':
    layer_var = 'cur'
#%%
var_path = r'C:\PROYECTOS\MEF\SCRIPT\DGPMI_CALIDAD_DATOS\variables.json'
var = get_json_file(var_path)
#%%
datasources_df_path = var['datasource_path'] + '\datasources.csv'
df_datasources = pd.read_csv(datasources_df_path)
#%% Filtro de las fuentes a procesar
df_datasources = df_datasources[df_datasources['status'] == 1]

#%%
j = 1
n = df_datasources.shape[0]
for i, row in df_datasources.iterrows():
    table_name = row['table_name_gx']
    print("\nGenerando Reporte ("+str(j)+"/"+str(n)+") de Validación de: ", row['data_source'].upper())
#%%
#table_name = "tr_proy_ano"
    my_checkpoint_name = "ckpt_" + layer_var +"_" + table_name

# In[19]:
    context.run_checkpoint(checkpoint_name=my_checkpoint_name)
#context.open_data_docs()
# In[ ]:
    print('Fin de la validación')
    j = j +1
time.sleep(3)

#%%