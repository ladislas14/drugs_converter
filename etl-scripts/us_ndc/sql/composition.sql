INSERT INTO composition (active_substance_id, drug_id, quantity, unit, reference)

SELECT
usinn.id,
drug.id,
CASE
	WHEN usp.strengh ~ '^([0-9 ]*)(\,|\.|)([0-9]*)\s+(.*)/(.*)$' THEN REGEXP_REPLACE(usp.strengh, '^([0-9 ]*)(\,|\.|)([0-9]*)\s+(.*)/(.*)$', '\1.\3')::double precision
	else null
END,
CASE
	WHEN usp.strengh ~ '^([0-9 ]*)(\,|\.|)([0-9]*)\s+(.*)/(.*)$' THEN REGEXP_REPLACE(usp.strengh, '^([0-9 ]*)(\,|\.|)([0-9]*)\s+(.*)/(.*)$', '\4')
	else null
END,
CASE
	WHEN usp.strengh ~ '^([0-9 ]*)(\,|\.|)([0-9]*)\s+(.*)/(.*)$' THEN REGEXP_REPLACE(usp.strengh, '^([0-9 ]*)(\,|\.|)([0-9]*)\s+(.*)/(.*)$', '\5')
	else null
END
FROM us_ndc.us_ingredients_products usp
JOIN us_ndc.us_inn_ingredients usinn ON (usinn.ingredient_name = lower(usp.ingredient_name))
JOIN drug ON (drug.source_id = usp.product_id)