select a.ano_ejec,a.fec_liquidacion,a.codigo_unico,a.id_cierre,a.id_etapa,a.flg_culminado,a.id_estado,a.flg_activo,a.cod_snip, to_char(now(),'dd/mm/yyyy hh24:mi:ss') fecha_carga
from landing.inv_cierre_inversion a
where a.codigo_unico is not null and a.id_cierre is not null
and a.cod_snip is not null and a.id_estado is not null and a.id_estado in (0,1) and a.flg_activo is not null and a.flg_activo in (0,1)