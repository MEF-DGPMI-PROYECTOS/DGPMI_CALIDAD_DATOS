select ano_eje, codigo_unico, estado_reg, fecha_validacion_brecha, to_date(fecha_viabilidad,'dd/mm/rrrr') fecha_viabilidad, id_brecha, id_idea, nombre_inversion, pim, programacion_inversion_anio0, programacion_inversion_anio1, programacion_inversion_anio2, programacion_inversion_anio3, tipo_no_prevista, validacion_brecha, version,
to_char(sysdate,'dd/mm/rrrr hh24:mi:ss') fecha_carga
from prg_cartera_inversion
where (ano_eje is null or ano_eje >=2005)
and codigo_unico is not null
and estado_reg is not null
and estado_reg in (0,1)
and (pim >=0 or pim is null)
and (programacion_inversion_anio0>=0 or programacion_inversion_anio0 is null)
and (tipo_no_prevista>=0 or tipo_no_prevista is null)
and validacion_brecha is not null
and (version is not null and version>0)