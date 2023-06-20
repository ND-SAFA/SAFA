/*
 Alter Table
 */
ALTER TABLE artifact_attribute_version
    ADD COLUMN attribute_value JSON;

/*
 Migrate simple data
 */
UPDATE artifact_attribute_version av, string_attribute_value sv
    SET av.attribute_value = JSON_QUOTE(sv.attribute_value)
    WHERE av.id = sv.attribute_version_id;

UPDATE artifact_attribute_version av, integer_attribute_value iv
    SET av.attribute_value = CAST(iv.attribute_value AS JSON)
    WHERE av.id = iv.attribute_version_id;

UPDATE artifact_attribute_version av, float_attribute_value fv
    SET av.attribute_value = CAST(fv.attribute_value AS JSON)
    WHERE av.id = fv.attribute_version_id;

UPDATE artifact_attribute_version av, boolean_attribute_value bv
    SET av.attribute_value = CAST(bv.attribute_value AS JSON)
    WHERE av.id = bv.attribute_version_id;

/*
 Migrate array data
 */
CREATE TEMPORARY TABLE list_values (
    id VARCHAR(255),
    attribute_value MEDIUMTEXT
);

INSERT INTO list_values
    SELECT saav.attribute_version_id, CONCAT('[', GROUP_CONCAT(JSON_QUOTE(saav.attribute_value) separator ','), ']')
    FROM string_array_attribute_value saav
    GROUP BY saav.attribute_version_id;

UPDATE artifact_attribute_version av, list_values lv
    SET av.attribute_value = lv.attribute_value
    WHERE av.id = lv.id;

/*
 Drop old tables
 */
DROP TABLE list_values;
DROP TABLE string_attribute_value;
DROP TABLE string_array_attribute_value;
DROP TABLE integer_attribute_value;
DROP TABLE float_attribute_value;
DROP TABLE boolean_attribute_value;