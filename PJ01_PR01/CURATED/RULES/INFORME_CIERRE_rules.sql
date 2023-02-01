WITH tbl_ini AS (
select cast(proyecto as integer) , to_char(now(),'dd/mm/yyyy hh24:mi:ss') fecha_carga from landing.informe_cierre
where proyecto is not null and proyecto > 0
),
dupli as(
select proyecto,count(1) as dupli from tbl_ini
group by proyecto) 
SELECT a.proyecto, fecha_carga from tbl_ini a  INNER JOIN dupli b
ON a.proyecto = b.proyecto 
WHERE b.Dupli=1
