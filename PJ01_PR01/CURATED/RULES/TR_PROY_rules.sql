WITH tbl_ini AS (
select cast (act_proy as integer) as act_proy,monto_devengado, to_char(now(),'dd/mm/yyyy hh24:mi:ss') fecha_carga  from landing.tr_proy
where act_proy is not null 
),
dupli as(
select act_proy,count(1) as dupli from tbl_ini
where act_proy > 0
group by act_proy) 
SELECT a.act_proy,monto_devengado, fecha_carga from tbl_ini a  INNER JOIN dupli b
ON a.act_proy = b.act_proy 
WHERE b.Dupli=1