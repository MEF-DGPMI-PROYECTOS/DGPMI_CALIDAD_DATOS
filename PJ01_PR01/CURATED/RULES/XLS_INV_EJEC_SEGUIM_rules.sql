select date(k.fec_ini_ej) fec_ini_ej,k.codigo_unico,k.avan_ejecuc,k.avan_estim,k.ultimo_devengado, to_char(now(),'dd/mm/yyyy hh24:mi:ss') fecha_carga
from landing.xls_inv_ejec_seguim k
where k.codigo_unico is not null and k.ultimo_devengado is not null and k.avan_estim is not null
and k.avan_estim is not null