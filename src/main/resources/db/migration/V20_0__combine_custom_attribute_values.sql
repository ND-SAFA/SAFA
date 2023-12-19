/*
 Alter Table
 */
ALTER TABLE artifact_attribute_version
    ADD COLUMN attribute_value MEDIUMTEXT;

/*
 Migrate simple data

 All the the ugliness here is because H2 does not support update with join or JSON_QUOTE
 */
UPDATE artifact_attribute_version av
SET av.attribute_value = CONCAT('"', REPLACE(
        (SELECT sv.attribute_value from string_attribute_value sv where sv.attribute_version_id = av.id), '"', '\\"'),
                                '"')
WHERE EXISTS (SELECT * from string_attribute_value sv WHERE av.id = sv.attribute_version_id);

UPDATE artifact_attribute_version av
SET av.attribute_value = CAST((SELECT iv.attribute_value
                               from integer_attribute_value iv
                               where iv.attribute_version_id = av.id) AS JSON)
WHERE EXISTS (SELECT * from integer_attribute_value iv WHERE av.id = iv.attribute_version_id);

UPDATE artifact_attribute_version av
SET av.attribute_value = CAST((SELECT fv.attribute_value
                               from float_attribute_value fv
                               where fv.attribute_version_id = av.id) AS JSON)
WHERE EXISTS (SELECT * from float_attribute_value fv WHERE av.id = fv.attribute_version_id);

UPDATE artifact_attribute_version av
SET av.attribute_value = CAST((SELECT bv.attribute_value
                               from boolean_attribute_value bv
                               where bv.attribute_version_id = av.id) AS JSON)
WHERE EXISTS (SELECT * from boolean_attribute_value bv WHERE av.id = bv.attribute_version_id);

/*
 Migrate array data
 */
CREATE TABLE list_values
(
    id              VARCHAR(255),
    attribute_value MEDIUMTEXT,
    primary key (id)
);

INSERT INTO list_values
SELECT saav.attribute_version_id,
       CONCAT('[', GROUP_CONCAT(CONCAT('"', REPLACE(saav.attribute_value, '"', '\\"'), '"') separator ','), ']')
FROM string_array_attribute_value saav
GROUP BY saav.attribute_version_id;

UPDATE artifact_attribute_version av
SET av.attribute_value = (SELECT lv.attribute_value from list_values lv where lv.id = av.id)
WHERE EXISTS (SELECT * from list_values lv WHERE av.id = lv.id);

/*
 Drop old tables
 */
DROP TABLE list_values;
DROP TABLE string_attribute_value;
DROP TABLE string_array_attribute_value;
DROP TABLE integer_attribute_value;
DROP TABLE float_attribute_value;
DROP TABLE boolean_attribute_value;
