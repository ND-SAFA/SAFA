package edu.nd.crc.safa.features.documents.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.features.documents.entities.app.DocumentColumnAppEntity;
import edu.nd.crc.safa.features.documents.entities.app.DocumentColumnDataType;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

@Entity
@Table(name = "document_column")
public class DocumentColumn {
    /**
     * Uniquely identifies every column in the database.
     */
    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column
    private UUID documentColumnId;
    /**
     * The name of the column to be displayed.
     */
    @Column(nullable = false)
    private String name;
    /**
     * The type of data this columns contains.
     */
    @Enumerated(EnumType.STRING)
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(nullable = false)
    private DocumentColumnDataType dataType;
    /**
     * The document containing this columns
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "document_id",
        nullable = false
    )
    private Document document;
    /**
     * The index this column is in the associated document above.
     */
    @Column(nullable = false)
    private int tableColumnIndex;
    /**
     * Whether this column should be required on rows in table.
     */
    @Column(nullable = false)
    private boolean required;

    public DocumentColumn() {
        this.required = false;
    }

    public DocumentColumn(DocumentColumnAppEntity documentColumnAppEntity, Document document, int tableColumnIndex) {
        this();
        this.documentColumnId = documentColumnAppEntity.getId();
        this.name = documentColumnAppEntity.getName();
        this.dataType = documentColumnAppEntity.getDataType();
        this.document = document;
        this.tableColumnIndex = tableColumnIndex;
        this.required = documentColumnAppEntity.isRequired();
    }

    public boolean isRequired() {
        return required;
    }

    public void setRequired(boolean required) {
        this.required = required;
    }

    public int getTableColumnIndex() {
        return tableColumnIndex;
    }

    public void setTableColumnIndex(int tableColumnIndex) {
        this.tableColumnIndex = tableColumnIndex;
    }

    public Document getDocument() {
        return document;
    }

    public void setDocument(Document document) {
        this.document = document;
    }

    public UUID getDocumentColumnId() {
        return documentColumnId;
    }

    public void setDocumentColumnId(UUID documentColumnId) {
        this.documentColumnId = documentColumnId;
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
