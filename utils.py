#%% TODO Librerias

import smtplib
import time
import json
import connectorx as cx
import numpy as np
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import datetime as dt
from pandas.core.dtypes.common import is_integer_dtype
import tqdm
import pandas_profiling
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import SET


#%%
class SendNotification:
    @staticmethod
    def send_email(in_file_name, in_attach_path, in_subject):
        FROM = 'calidad_datos_invierte@mef.gob.pe'
        to = ['Consultor_C2_CC01@mef.gob.pe']
        #to = ['serviciodeayuda6@minedu.gob.pe']
        subject = in_subject
        body = 'Estimados por favor revisar el archivo adjunto correspondiente a la calidad de los datos.'
        firm = '<br/><br/>Saludos cordiales.<h6>Correo generado automáticamente</h6>'
        print(to)
        time.sleep(15)
        body = body + firm

        attachment_name = in_file_name

        # todo Multipart
        message = MIMEMultipart()
        message['From'] = FROM
        message['To'] = ", ".join(to)
        message['Subject'] = subject

        message.attach(MIMEText(body, 'html'))

        attachment_file = open(in_attach_path, 'rb')

        attachment_mime = MIMEBase('application', 'octect-stream')

        attachment_mime.set_payload(attachment_file.read())
        encoders.encode_base64(attachment_mime)
        attachment_mime.add_header('Content-Disposition', "attachment; filename= %s" % attachment_name)

        message.attach(attachment_mime)

        server = "correo.mef.gob.pe"
        server = smtplib.SMTP(server)
        # server.starttls()
        # server.ehlo()

        message_text = message.as_string()

        server.sendmail(FROM, to, message_text)
        server.quit()

#%%
#%% TODO Functions
def get_json_file(var_path):
    with open(var_path) as json_file:
        var = json.load(json_file)
    return var

def read_sql_file(sql):

    output =  open(sql, mode='r', encoding='utf-8').read()
    return output

def get_data_sql(engine, sql):
    dff = cx.read_sql(engine, sql)
    return dff

def engine_sch_psql_schema(conn_dl_psycopg):
    try:
        return create_engine(conn_dl_psycopg)
    except Exception as e:
        print(e.args)

def get_file_key(key_file_path):
    with open(key_file_path, 'rb') as filekey:
        key = filekey.read()
    return key

def to_landing_layer(datasource_sql_files, df_datasources, conn_ds, landing_path, conn_dl):
    now_i = datetime.now()
    print('1. Start time global: ', now_i)
    for i in tqdm.tqdm(datasource_sql_files):
        try:
            name = (i.split('\\')[-1]).split('.')[0]
            now = datetime.now()
            print("\n***************************************************************")
            print("Reading data: ", name)
            print('Start time: ', now)
            sql_i = read_sql_file(i)
            if name.lower() in list(df_datasources['data_source']):
                df_load = df_datasources[df_datasources['data_source'] == name.lower()]
                if list(df_load['process_type'])[0] == 'incremental':
                    filter = list(df_load['filter'])[0]
                    sql_i = sql_i + ' where ' + filter + ' = ' + str(var['date_delta_monthly'])
                    name = name + '_delta'
            df_i = get_data_sql(conn_ds, sql_i)
            df_i.columns =  df_i.columns.str.lower()
            print("\nShape: ", df_i.shape)
            print('Before optimization:\n', df_i.dtypes)
            fcols = df_i.select_dtypes('float').columns
            icols = df_i.select_dtypes('integer').columns
            print('Float columns: ', fcols)
            print('Int columns: ', icols)
            df_i[fcols] = df_i[fcols].apply(pd.to_numeric, downcast='float')
            df_i[icols] = df_i[icols].apply(pd.to_numeric, downcast='integer')
            print('After optimization:\n', df_i.dtypes)
            print('Memory usage (MB): ', np.round(df_i.memory_usage().sum() / 10**6, 3))
            path_i_export = landing_path + '\\' + name + '.parquet'
            df_i.to_parquet(path_i_export, engine='pyarrow', compression='snappy')
            print('....')
            df_i.to_sql(name=name.lower(), schema='landing', con=conn_dl, if_exists='replace', index=False)
            print('\nDataframe exported to the landing layer')
            del df_i
            print('Finish time: ', datetime.now())
            print('Duration: ', datetime.now() - now)
        except Exception as e:
            print(e.args)
    print('2. Finish time global: ', datetime.now())
    print('Duration: ', datetime.now() - now_i)

def to_curated_layer(curated_rule_sql_files, df_correct_datatypes, conn_ds, conn_dl):
    now_i = datetime.now()
    print('1. Start time global: ', now_i)
    for i in tqdm.tqdm(curated_rule_sql_files):
        try:
            name = (i.split('\\')[-1]).split('.')[0]
            name = name.replace("_rules", "")
            now = datetime.now()
            print("\n***************************************************************")
            print('Transforming table: ', name)
            print("Reading data: ", name)
            print('Start time: ', now)
            sql_i = read_sql_file(i)
            df_trans = get_data_sql(conn_ds, sql_i)
            df_trans.columns = df_trans.columns.str.lower()
            fcols = df_trans.select_dtypes('float').columns
            icols = df_trans.select_dtypes('integer').columns
            df_trans[fcols] = df_trans[fcols].apply(pd.to_numeric, downcast='float')
            df_trans[icols] = df_trans[icols].apply(pd.to_numeric, downcast='integer')

            df_columns = pd.DataFrame(df_trans.columns, columns=['column_name'])

            df_inner = df_correct_datatypes.merge(df_columns, how='inner', on='column_name')

            for index, row in df_inner.iterrows():
                if row['data_type'] == 'int':
                    if not is_integer_dtype(df_trans.dtypes[row['column_name']]):
                        print('Transforming data types')
                        df_trans[row['column_name']] = df_trans[row['column_name']].fillna(0).astype(row['data_type'])
                        print(df_trans.dtypes)

            df_trans['fecha_carga'] = dt.datetime.today().strftime("%d/%m/%Y %H:%M:%S")
            print('\nExporting dataframe...')
            df_trans.to_sql(name=name.lower(), schema='curated', con=conn_dl, if_exists='replace', index=False)
            print('\nDataframe exported to the curated layer')
            del df_trans
            print('Finish time: ', datetime.now())
            print('Duration: ', datetime.now() - now)
        except Exception as e:
            print(e.args)
    print('2. Finish time global: ', datetime.now())
    print('Duration: ', datetime.now() - now_i)

def to_functional_layer(kpi_sql_files, conn_dl):
    now_i = datetime.now()
    print('1. Start time global: ', now_i)
    for i in tqdm.tqdm(kpi_sql_files):
        try:
            name = (i.split('\\')[-1]).split('.')[0]
            now = datetime.now()
            print("\n***************************************************************")
            print("Reading data: ", name)
            print('Start time: ', now)
            sql_i = read_sql_file(i)
            df_i = get_data_sql(conn_dl, sql_i)
            df_i.columns =  df_i.columns.str.lower()
            print("\nShape: ", df_i.shape)
            print('Before optimization:\n', df_i.dtypes)
            fcols = df_i.select_dtypes('float').columns
            icols = df_i.select_dtypes('integer').columns
            print('Float columns: ', fcols)
            print('Int columns: ', icols)
            df_i[fcols] = df_i[fcols].apply(pd.to_numeric, downcast='float')
            df_i[icols] = df_i[icols].apply(pd.to_numeric, downcast='integer')
            print('After optimization:\n', df_i.dtypes)
            print('Memory usage (MB): ', np.round(df_i.memory_usage().sum() / 10**6, 3))

            df_i.to_sql(name=name.lower(), schema='functional', con=conn_dl, if_exists='replace', index=False)
            print('\nDataframe exported to the functional layer')
            del df_i
            print('Finish time: ', datetime.now())
            print('Duration: ', datetime.now() - now)
        except Exception as e:
            print(e.args)
    print('2. Finish time global: ', datetime.now())
    print('Duration: ', datetime.now() - now_i)

def to_profiling_report(datasource_sql_files, profiling_report_path, conn_ds):
    now_i = datetime.now()
    print('1. Start time global: ', now_i)
    for i in tqdm.tqdm(datasource_sql_files):
        try:
            name = (i.split('\\')[-1]).split('.')[0]
            now = datetime.now()
            print("\n***************************************************************")
            print("Reading data: ", name)
            print('Start time: ', now)
            sql_i = read_sql_file(i)
            df_i = get_data_sql(conn_ds, sql_i)
            print("\nShape: ", df_i.shape)
            fcols = df_i.select_dtypes('float').columns
            icols = df_i.select_dtypes('integer').columns
            df_i[fcols] = df_i[fcols].apply(pd.to_numeric, downcast='float')
            df_i[icols] = df_i[icols].apply(pd.to_numeric, downcast='integer')
            print('Memory usage (MB): ', np.round(df_i.memory_usage().sum() / 10 ** 6, 3))
            path_i_export = profiling_report_path + '\\Profile_' + name + '.html'
            profile = pandas_profiling.ProfileReport(df_i, title="Profiling Report - " + name.upper())
            profile.to_file(output_file=path_i_export)
            print('\nProfiling report exported')
            del df_i
            print('Finish time: ', datetime.now())
            print('Duration: ', datetime.now() - now)
        except Exception as e:
            print(e.args)
    print('2. Finish time global: ', datetime.now())
    print('Duration: ', datetime.now() - now_i)
