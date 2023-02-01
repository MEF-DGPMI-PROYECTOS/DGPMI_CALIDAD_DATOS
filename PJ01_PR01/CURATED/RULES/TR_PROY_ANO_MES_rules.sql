WITH tbl_ini AS (
SELECT cast(act_proy as integer) act_proy ,ANO_EJE,MES_EJE,MONTO_DEVENGADO,cast(TIPO_ACT_PROY as integer) tipo_act_proy,MONTO_PIM, to_char(now(),'dd/mm/yyyy hh24:mi:ss') fecha_carga
FROM landing.TR_PROY_ANO_MES
WHERE ANO_EJE IS NOT NULL AND 
MES_EJE IS NOT NULL AND ACT_PROY IS NOT NULL AND TIPO_ACT_PROY IS NOT NULL
),
dupli as(
SELECT ACT_PROY,ANO_EJE,MES_EJE,TIPO_ACT_PROY,count(1) AS Dupli FROM tbl_ini
GROUP BY ACT_PROY,ANO_EJE,MES_EJE,TIPO_ACT_PROY)
SELECT a.ACT_PROY,a.ANO_EJE,a.MES_EJE,a.MONTO_DEVENGADO,a.TIPO_ACT_PROY,a.MONTO_PIM, fecha_carga FROM tbl_ini a  INNER JOIN dupli b
ON a.ACT_PROY = b.ACT_PROY AND a.ANO_EJE=b.ANO_EJE AND a.MES_EJE=b.MES_EJE AND a.TIPO_ACT_PROY=b.TIPO_ACT_PROY
WHERE b.Dupli=1