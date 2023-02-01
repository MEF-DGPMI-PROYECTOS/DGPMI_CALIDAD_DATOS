SELECT   id_corte,cast(periodo as integer) periodo,cast(estado as integer) estado,nombre,date(fecha_corte_inicio) fecha_corte_inicio, date(fecha_corte_fin) fecha_corte_fin, to_char(now(),'dd/mm/yyyy hh24:mi:ss') fecha_carga
from landing.prg_corte_registro
where
id_corte IS NOT NULL and id_corte >0
AND estado IN (0,1)