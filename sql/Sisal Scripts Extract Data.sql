/*QUERY 1 — ISÓTOPOS */

SELECT
    e.entity_name,
    oc.interp_age,
    o18.d18O_measurement,
    o18.d18O_precision,
    c13.d13C_measurement,
    c13.d13c_precision,
    s.depth_sample
FROM site si
LEFT JOIN entity e USING (site_id)
LEFT JOIN sample s USING (entity_id)
LEFT JOIN d18O o18 USING (sample_id)
LEFT JOIN d13c c13 USING (sample_id)
LEFT JOIN original_chronology oc USING (sample_id)
WHERE si.site_name = 'Botuvera Cave';


/*QUERY 2 — DATAÇÃO*/

SELECT
     e.entity_name,
     d.lab_num,
     d.depth_dating,
     d.corr_age,
     d.corr_age_uncert_pos
 FROM site si
 LEFT JOIN entity e USING (site_id)
 LEFT JOIN dating d USING (entity_id)
 WHERE si.site_name = 'Shatuca Cave';

/*    QUERY 3 — REFERÊNCIAS DO SITE */
 SELECT
     e.entity_name,
     r.ref_id,
     r.citation,
     r.publication_DOI
 FROM site si
 LEFT JOIN entity e USING (site_id)
 LEFT JOIN entity_reference_link erl
     ON erl.entity_id = e.entity_id
 LEFT JOIN reference r
     ON r.ref_id = erl.ref_id
 WHERE si.site_name = 'Shatuca Cave';

