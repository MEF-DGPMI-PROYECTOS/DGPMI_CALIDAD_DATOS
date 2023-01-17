select pb.codigo_unico,pb.monto,pb.monto_viable,pb.dev_año_actual,pb.pim_año_actual,pb.dev dev_acumulado,
pb.nivel,pb.pliego_opmi,pb.funcion,pb.programa,pb.subprogram,pb.des_tipo_formato, esconder, 
pb.estado, pb.situacion,to_char(sysdate,'dd/mm/rrrr hh24:mi:ss') fecha_carga 
from xls_proyecto_banco pb
where pb.codigo_unico is not null
   and (pb.monto is  null or pb.monto>0)
   and (pb.dev_año_actual is null or pb.dev_año_actual>0)
   and (pb.pim_año_actual is null or pb.pim_año_actual>0)