select
act_proy,
ano_eje,
mes_eje,
monto_devengado,
tipo_act_proy,
monto_pim,
to_char(sysdate,'dd/mm/rrrr hh24:mi:ss') fecha_carga
from
tr_proy_ano_mes