WITH tbl_ini AS (
select cast (cod_idea as integer) as cod_idea,ano_eje,des_nombre,id_idea,fec_crea, to_char(now(),'dd/mm/yyyy hh24:mi:ss') fecha_carga from landing.INV_IDEA
where cod_idea is not null and ano_eje > 0 and ano_eje is not null
),
dupli as(
select ano_eje,cod_idea,count(1) as dupli from tbl_ini
where cod_idea > 0
group by ano_eje,cod_idea) 
SELECT a.ano_eje,a.cod_idea,des_nombre,id_idea,fec_crea, fecha_carga  from tbl_ini a  INNER JOIN dupli b
ON a.cod_idea = b.cod_idea 
WHERE b.Dupli=1