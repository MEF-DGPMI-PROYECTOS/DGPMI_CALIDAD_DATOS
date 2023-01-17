SELECT   id_corte,periodo,estado,nombre,fecha_corte_inicio,fecha_corte_fin,fecha_corte_fin_crono,
to_char(sysdate,'dd/mm/rrrr hh24:mi:ss') fecha_carga
from prg_corte_registro
where
id_corte IS NOT NULL
AND estado IN (0,1)