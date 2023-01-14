with ult_version as (
select id_corte as id_version, nombre,fecha_corte_inicio, 
row_number() over(
        partition by periodo
        order by  fecha_corte_fin desc
    ) as row_num,fecha_corte_fin,periodo

from curated.prg_corte_registro 
where fecha_corte_fin is not null and periodo >=2018 and periodo = extract (year from fecha_corte_fin)
),
tbl_pro as (
select xpb.codigo_unico,ip.val_beneficiario_ultimo ,xpb.monto,ver.id_version,ver.fecha_corte_fin,
row_number() over(
        partition by xpb.codigo_unico
        order by ver.fecha_corte_fin desc 
    ) ult_program_pmi
from curated.xls_proyecto_banco xpb inner join curated.prg_cartera_inversion cart
on xpb.codigo_unico = cart.codigo_unico inner join (select id_version,fecha_corte_fin from ult_version where row_num = 1)  ver
on ver.id_version = cart.version   inner  join curated.inv_proyecto ip
on ip.cod_unico = xpb.codigo_unico  
where cart.estado_reg = 1 and UPPER(xpb.estado) in ('CERRADO','ACTIVO') and xpb.esconder =0 and COALESCE(ip.val_beneficiario_ultimo,0) >0
)

select codigo_unico,monto,val_beneficiario_ultimo,id_version,
(monto/val_beneficiario_ultimo) as i10_monto_x_benef from tbl_pro
where ult_program_pmi = 1
