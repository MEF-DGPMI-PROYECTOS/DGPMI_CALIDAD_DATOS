select
monto,
estado,
pim_año_actual pim_ano_actual,
codigo_unico,
monto_viable,
dev_año_actual dev_ano_actual,
dev dev_acumulado,
situacion,
año_viab ano_viab,
fecha_regi,
fecha_viab,
tipo_formato,
esconder,
des_cierre,
cerrado,
monto_laudo,
monto_fianza,
to_char(sysdate,'dd/mm/rrrr hh24:mi:ss') fecha_carga
from xls_proyecto_banco
