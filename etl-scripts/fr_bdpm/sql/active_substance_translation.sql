INSERT INTO active_substance_translation (active_substance_id, name, country_id)

SELECT inns.id, inns.french_name, '1' FROM inn.inns WHERE inns.id IN (SELECT id FROM fr_bdpm.fr_inn_ingredients)