package edu.nd.crc.safa.features.documents.entities.app;

import java.util.UUID;

import edu.nd.crc.safa.features.documents.entities.db.DocumentColumn;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Represents the front-end column data for a FMEA table.
 */
@Data
@NoArgsConstructor
public class DocumentColumnAppEntity {
    /**
     * Uniquely identifies every column in the database.
     */
    private UUID id;
    /**
     * The name of the column
     */
    private String name;
    /**
     * The type of data this column contains
     */
    private DocumentColumnDataType dataType;
    /**
     * Whether this column is required to create artifacts.
     */
    private boolean required = false;

    public DocumentColumnAppEntity(DocumentColumn documentColumn) {
        this();
        this.id = documentColumn.getDocumentColumnId();
        this.name = documentColumn.getName();
        this.dataType = documentColumn.getDataType();
        this.required = documentColumn.isRequired();
    }
}
