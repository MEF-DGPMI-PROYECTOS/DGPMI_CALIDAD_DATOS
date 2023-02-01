select  f.id_exp_tecnico,f.id_exp_tecnico_seg,  to_char(now(),'dd/mm/yyyy hh24:mi:ss') fecha_carga
from landing.inv_exp_tecnico_seg f
where  f.id_exp_tecnico is not null and f.id_exp_tecnico_seg is not null
