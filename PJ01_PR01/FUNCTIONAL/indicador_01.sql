select codigo_unico,
       monto_devengado,
       version,
       --nombre_corte,
       programacion_inversion_anio0 monto_pmi_anio_vigente,
       case when (programacion_inversion_anio0 is null or programacion_inversion_anio0 = 0) then -999
       else round( cast((monto_devengado / programacion_inversion_anio0) * 100 as decimal), 2) end indicador_01
  from (select ci.version, 
               cr.nombre nombre_corte,
               cr.estado estado_corte,
               cr.periodo ano_proceso,
               pa.monto_devengado,
               codigo_unico,
               ci.estado_reg estado_pi,                                 
               nombre_inversion,
               programacion_inversion_anio0
          from curated.prg_cartera_inversion ci
               left join curated.prg_corte_registro cr on ci.version = cr.id_corte
               left join curated.tr_proy_ano pa
                  on     ci.codigo_unico = pa.act_proy
                     and cr.periodo = pa.ano_eje) t
 where estado_corte = 1
