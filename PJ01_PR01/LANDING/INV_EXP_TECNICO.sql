SELECT E.COD_UNICO CODIGO_UNICO,E.FEC_APROBACION,E.FEC_CREA,E.FLG_ACTIVO, to_char(sysdate,'dd/mm/rrrr hh24:mi:ss') fecha_carga
FROM ODI.INV_EXP_TECNICO E