select
id_corte,
periodo,
estado,
nombre,
fecha_corte_inicio,
fecha_corte_fin, 
to_char(sysdate,'dd/mm/rrrr hh24:mi:ss') fecha_carga
from prg_corte_registro