select 
cod_unico codigo_unico, monto_ejec, monto_viabil, num_plazo_ejec, num_plazo_viabil, to_char(sysdate,'dd/mm/rrrr hh24:mi:ss') fecha_carga
from inv_detalle_cierre_expost