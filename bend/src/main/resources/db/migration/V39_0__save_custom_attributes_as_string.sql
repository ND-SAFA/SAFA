ALTER TABLE artifact_body
    ADD COLUMN custom_attributes MEDIUMTEXT;

DROP TABLE artifact_attribute_version;
