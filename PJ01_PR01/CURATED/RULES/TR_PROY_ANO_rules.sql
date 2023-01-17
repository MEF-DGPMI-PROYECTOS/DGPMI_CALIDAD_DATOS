select act_proy, ano_eje, monto_devengado, monto_pim, tipo_act_proy, to_char(sysdate,'dd/mm/rrrr hh24:mi:ss') fecha_carga
from tr_proy_ano
where act_proy is not null
and (ano_eje is not null and ano_eje>=2004)
and (monto_devengado is not null and monto_devengado>=0)
and (monto_pim is not null and monto_pim>=0)
and tipo_act_proy is not null