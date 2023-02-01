WITH tbl_ini AS (
select cast(id_etapa as integer) id_etapa, to_char(now(),'dd/mm/yyyy hh24:mi:ss') fecha_carga from landing.inv_etapa
where id_etapa is not null and id_etapa > 0
),
dupli as(
select id_etapa,count(1) as dupli from tbl_ini
group by id_etapa) 
SELECT a.id_etapa, fecha_carga from tbl_ini a  INNER JOIN dupli b
ON a.id_etapa = b.id_etapa 
WHERE b.Dupli=1
