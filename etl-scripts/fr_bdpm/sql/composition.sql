INSERT INTO composition (quantity, unit, drug_id, active_substance_id, reference)

SELECT 
CASE 
	WHEN fr_cis_compo_bdpm."Dosage de la substance" ~ '^([0-9 ]*)(\,|\.|)([0-9]*)( *mg)(.*)$' THEN REGEXP_REPLACE(REGEXP_REPLACE(fr_cis_compo_bdpm."Dosage de la substance",'^([0-9 ]*)(\,|\.|)([0-9]*)( *mg)(.*)$','\1.\3'), '\s+', '', 'g')::double precision
	WHEN fr_cis_compo_bdpm."Dosage de la substance" ~ '^([0-9 ]*)(\,|\.|)([0-9]*)( *g)(.*)$' THEN REGEXP_REPLACE(REGEXP_REPLACE(fr_cis_compo_bdpm."Dosage de la substance",'^([0-9 ]*)(\,|\.|)([0-9]*)( *g)(.*)$','\1.\3'), '\s+', '', 'g')::double precision
	WHEN fr_cis_compo_bdpm."Dosage de la substance" ~ '^([0-9 ]*)(\,|\.|)([0-9]*)( *ml)(.*)$' THEN REGEXP_REPLACE(REGEXP_REPLACE(fr_cis_compo_bdpm."Dosage de la substance",'^([0-9 ]*)(\,|\.|)([0-9]*)( *ml)(.*)$','\1.\3'), '\s+', '', 'g')::double precision
	WHEN fr_cis_compo_bdpm."Dosage de la substance" ~ '^([0-9 ]*)(\,|\.|)([0-9]*)( *microgramme)(.*)$' THEN REGEXP_REPLACE(REGEXP_REPLACE(fr_cis_compo_bdpm."Dosage de la substance",'^([0-9 ]*)(\,|\.|)([0-9]*)( *microgramme)(.*)$','\1.\3'), '\s+', '', 'g')::double precision
	WHEN fr_cis_compo_bdpm."Dosage de la substance" ~ '^([0-9 ]*)(\,|\.|)([0-9]*)( *U(\.|)(I|l)(\.|))(.*)$' THEN REGEXP_REPLACE(REGEXP_REPLACE(fr_cis_compo_bdpm."Dosage de la substance",'^([0-9 ]*)(\,|\.|)([0-9]*)( *U(\.|)(I|l)(\.|))(.*)$','\1'), '\s+', '', 'g')::double precision
	WHEN fr_cis_compo_bdpm."Dosage de la substance" ~ '^([0-9 ]*)(\,|\.|)([0-9]*)( *M(\.|)U(\.|)(I|l)(\.|))$' THEN REGEXP_REPLACE(REGEXP_REPLACE(fr_cis_compo_bdpm."Dosage de la substance",'^([0-9 ]*)(\,|\.|)([0-9]*)( *M(\.|)U(\.|)(I|l)(\.|))$','\1.\3'), '\s+', '', 'g')::double precision
	WHEN fr_cis_compo_bdpm."Dosage de la substance" ~ '^([0-9 ]*)(\,|\.|)([0-9]*)( *%)(.*)$' THEN REGEXP_REPLACE(REGEXP_REPLACE(fr_cis_compo_bdpm."Dosage de la substance",'^([0-9 ]*)(\,|\.|)([0-9]*)( *%)(.*)$','\1.\3'), '\s+', '', 'g')::double precision
	ELSE null
END
,
CASE 
	WHEN fr_cis_compo_bdpm."Dosage de la substance" ~ '^([0-9 ]*)(\,|\.|)([0-9]*)( *mg)(.*)$' THEN 'mg'
	WHEN fr_cis_compo_bdpm."Dosage de la substance" ~ '^([0-9 ]*)(\,|\.|)([0-9]*)( *g)(.*)$' THEN 'g'
	WHEN fr_cis_compo_bdpm."Dosage de la substance" ~ '^([0-9 ]*)(\,|\.|)([0-9]*)( *ml)(.*)$' THEN 'ml'
	WHEN fr_cis_compo_bdpm."Dosage de la substance" ~ '^([0-9 ]*)(\,|\.|)([0-9]*)( *microgramme)(.*)$' THEN 'μg'
	WHEN fr_cis_compo_bdpm."Dosage de la substance" ~ '^([0-9 ]*)(\,|\.|)([0-9]*)( *U(\.|)(I|l)(\.|))(.*)$' THEN 'U.I.'
	WHEN fr_cis_compo_bdpm."Dosage de la substance" ~ '^([0-9 ]*)(\,|\.|)([0-9]*)( *M(\.| |)U(\.|)(I|l)(\.|))$' THEN 'M.U.I.'
	WHEN fr_cis_compo_bdpm."Dosage de la substance" ~ '^([0-9 ]*)(\,|\.|)([0-9]*)( *%)(.*)$' THEN '%'
	ELSE 'false'
END,
d.id,
fr_bdpm.fr_inn_ingredients.id,
CASE 
	WHEN fr_cis_compo_bdpm."Référence de ce dosage" ~ 'un.*' THEN '1'
	WHEN fr_cis_compo_bdpm."Référence de ce dosage" ~ '^[0-9]*\s+[a-zA-Z]*\s*.*$' THEN REGEXP_REPLACE(fr_cis_compo_bdpm."Référence de ce dosage",'^([0-9]*)\s+([a-zA-Z]*)\s*.*$', '\1 \2')
	ELSE null
END
FROM fr_bdpm.fr_cis_compo_bdpm
JOIN fr_bdpm.fr_inn_ingredients ON (fr_cis_compo_bdpm."Code de la substance" = fr_inn_ingredients.ingredient_id)
JOIN drug d ON (d.source_id = fr_cis_compo_bdpm."Code CIS"::text)