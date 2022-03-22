package edu.nd.crc.safa.server.entities.app;

import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.DocumentColumn;

/**
 * Represents the front-end column data for a FMEA table.
 */
public class DocumentColumnAppEntity {
    /**
     * Uniquely identifies every column in the database.
     */
    UUID id;
    /**
     * The name of the column
     */
    String name;
    /**
     * The type of data this column contains
     */
    DocumentColumnDataType dataType;
    /**
     * Whether this column is required to create artifacts.
     */
    boolean required;

    public DocumentColumnAppEntity() {
        this.required = false;
    }

    public DocumentColumnAppEntity(DocumentColumn documentColumn) {
        this();
        this.id = documentColumn.getDocumentColumnId();
        this.name = documentColumn.getName();
        this.dataType = documentColumn.getDataType();
        this.required = documentColumn.isRequired();
    }

    public boolean isRequired() {
        return required;
    }

    public void setRequired(boolean required) {
        this.required = required;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public DocumentColumnDataType getDataType() {
        return dataType;
    }

    public void setDataType(DocumentColumnDataType dataType) {
        this.dataType = dataType;
    }
}
