select cod_unico codigo_unico, to_date(fec_viabil,'dd/mm/rrrr') fec_viabil, id_cartera_inversion, id_estado, val_beneficiario_ultimo,
to_char(sysdate,'dd/mm/rrrr hh24:mi:ss') fecha_carga
from inv_proyecto
where cod_unico is not null
and (id_cartera_inversion >= 0 or id_cartera_inversion is null)
and id_estado is not null
and (val_beneficiario_ultimo >= 0 or val_beneficiario_ultimo is null)
