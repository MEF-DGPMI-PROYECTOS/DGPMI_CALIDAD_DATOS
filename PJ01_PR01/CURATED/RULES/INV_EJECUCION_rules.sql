select d.codigo_unico,d.monto_inversion,d.fec_asignacion,d.ano_ejec,d.flg_activo,d.cod_snip,d.num_version,d.id_ejecucion,d.id_etapa,to_char(now(),'dd/mm/yyyy hh24:mi:ss') fecha_carga
from landing.inv_ejecucion d 
where d.codigo_unico is not null and d.monto_inversion is not null and d.id_ejecucion is not null and d.flg_activo<8 and d.ano_ejec>=2018