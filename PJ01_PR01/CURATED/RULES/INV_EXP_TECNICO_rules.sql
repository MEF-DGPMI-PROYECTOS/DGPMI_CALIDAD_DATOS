select  e.codigo_unico,e.fec_aprobacion,e.fec_crea,e.flg_activo, to_char(now(),'dd/mm/yyyy hh24:mi:ss') fecha_carga
from landing.inv_exp_tecnico e
where e.codigo_unico is not null and e.flg_activo is not null and e.flg_activo in (0,1)