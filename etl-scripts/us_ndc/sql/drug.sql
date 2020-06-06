INSERT INTO drug(name, brand_name, country_id, source_id)

SELECT
DISTINCT ON (p.product_id)
p.generic_name,
p.brand_name,
4,
p.product_id
FROM us_ndc.us_products p
JOIN us_ndc.us_ingredients_products ip on (p.product_id = ip.product_id)
WHERE lower(ip.ingredient_name) IN (SELECT us_inn_ingredients.ingredient_name FROM us_ndc.us_inn_ingredients)