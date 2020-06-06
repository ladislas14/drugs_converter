INSERT INTO active_substance_translation (active_substance_id, name, country_id)

SELECT
inns.id,
inns.us_name,
'4'
FROM us_ndc.us_inn_ingredients
JOIN inn.inns on (inns.id = us_inn_ingredients.id)