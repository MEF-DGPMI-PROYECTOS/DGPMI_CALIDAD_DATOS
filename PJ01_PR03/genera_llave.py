#%% TODO Importa librerías
from cryptography.fernet import Fernet
import json
import os
#%% TODO Lectura de variables

var_path = r'C:\PROYECTOS\MEF\SCRIPT\DGPMI_CALIDAD_DATOS\variables.json'

with open(var_path) as json_file:
    var = json.load(json_file)

#%% TODO Genera llave
key_file_path = var['key_path'] + '\\'+ 'filekey.key'

if os.path.exists(key_file_path):
    print('La llave de encriptación ya existe.')
    print('La ruta es: ', key_file_path)
else:
    key = Fernet.generate_key()
    with open(key_file_path, 'wb') as filekey:
        filekey.write(key)
    print('Llave generada en: ', key_file_path)
