select act_proy, ano_eje, monto_devengado, monto_pim, tipo_act_proy,
to_char(sysdate,'dd/mm/rrrr hh24:mi:ss') fecha_carga
from tr_proy_ano