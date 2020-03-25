 SELECT us_drug_ndc_json.drug ->> 'product_id'::text AS product_id,
    us_drug_ndc_json.drug -> 'openfda' ->> 'is_original_packager' as is_original_packager,
    us_drug_ndc_json.drug -> 'openfda' ->> 'manufacturer_name' as manufacturer_name,
    us_drug_ndc_json.drug -> 'openfda' ->> 'nui' as nui,
    us_drug_ndc_json.drug -> 'openfda' ->> 'pharm_class_cs' as pharm_class_cs,
    us_drug_ndc_json.drug -> 'openfda' ->> 'pharm_class_epc' as pharm_class_epc,
    us_drug_ndc_json.drug -> 'openfda' ->> 'pharm_class_moa' as pharm_class_moa,
    us_drug_ndc_json.drug -> 'openfda' ->> 'pharm_class_pe' as pharm_class_pe,
    us_drug_ndc_json.drug -> 'openfda' ->> 'rxcui' as rxcui,
    us_drug_ndc_json.drug -> 'openfda' ->> 'spl_set_id' as spl_set_id,
    us_drug_ndc_json.drug -> 'openfda' ->> 'unii' as unii,
    us_drug_ndc_json.drug -> 'openfda' ->> 'upc' as upc
FROM us_ndc.us_drug_ndc_json;