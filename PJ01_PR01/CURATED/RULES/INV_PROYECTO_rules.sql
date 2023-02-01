select distinct codigo_unico, date(fec_viabil) fec_viabil, id_cartera_inversion, id_estado, val_beneficiario_ultimo,
to_char(now(),'dd/mm/yyyy hh24:mi:ss') fecha_carga
from landing.inv_proyecto
where codigo_unico is not null
and (id_cartera_inversion >= 0 or id_cartera_inversion is null)
and id_estado is not null
and (val_beneficiario_ultimo >= 0 or val_beneficiario_ultimo is null)