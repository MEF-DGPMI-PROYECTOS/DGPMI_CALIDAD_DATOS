WITH tbl_ini AS (
select cast(id_parametro as integer) id_parametro, to_char(now(),'dd/mm/yyyy hh24:mi:ss') fecha_carga from landing.inv_parametros
where id_parametro is not null and id_parametro > 0
),
dupli as(
select id_parametro,count(1) as dupli from tbl_ini
group by id_parametro) 
SELECT a.id_parametro, fecha_carga from tbl_ini a  INNER JOIN dupli b
ON a.id_parametro = b.id_parametro 
WHERE b.Dupli=1
