SELECT F.ID_EXP_TECNICO,F.ID_EXP_TECNICO_SEG, to_char(sysdate,'dd/mm/rrrr hh24:mi:ss') fecha_carga
FROM ODI.INV_EXP_TECNICO_SEG F 