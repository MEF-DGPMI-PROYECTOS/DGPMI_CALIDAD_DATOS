select distinct codigo_unico, monto_ejec, monto_viabil, num_plazo_ejec, num_plazo_viabil, to_char(now(),'dd/mm/yyyy hh24:mi:ss') fecha_carga
from landing.inv_detalle_cierre_expost
where codigo_unico is not null
and (monto_ejec is not null and monto_ejec>=0)
and (num_plazo_ejec >= 0 or num_plazo_ejec is null)
and (num_plazo_viabil >= 0 or num_plazo_viabil is null)
and (monto_viabil >= 0 or monto_viabil is null)