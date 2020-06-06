INSERT INTO drug(name, brand_name, country_id, source_id)

SELECT DISTINCT fr_cis_bdpm."Dénomination du médicament" as name, fr_cis_bdpm."Titulaire(s)" as brand_name, 1, fr_cis_bdpm."Code CIS" as source_id FROM fr_bdpm.fr_cis_bdpm
JOIN fr_bdpm.fr_cis_compo_bdpm ON (fr_bdpm.fr_cis_bdpm."Code CIS" = fr_bdpm.fr_cis_compo_bdpm."Code CIS")
WHERE fr_cis_compo_bdpm."Code de la substance" IN (SELECT ingredient_id FROM fr_bdpm.fr_inn_ingredients)