/*
 TODO: Migrate data instead of just wiping it
 */

DELETE FROM artifact_attribute_version;

ALTER TABLE artifact_attribute_version
    ADD COLUMN attribute_value MEDIUMTEXT;

DROP TABLE string_attribute_value;
DROP TABLE string_array_attribute_value;
DROP TABLE integer_attribute_value;
DROP TABLE float_attribute_value;
DROP TABLE boolean_attribute_value;