package edu.nd.crc.safa.server.entities.db;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.server.entities.app.DocumentColumnAppEntity;
import edu.nd.crc.safa.server.entities.app.DocumentColumnDataType;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

@Entity
@Table(name = "document_column")
public class DocumentColumn {
    /**
     * Uniquely identifies every column in the database.
     */
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column
    UUID documentColumnId;
    /**
     * The name of the column to be displayed.
     */
    @Column(nullable = false)
    String name;
    /**
     * The type of data this columns contains.
     */
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    DocumentColumnDataType dataType;
    /**
     * The document containing this columns
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "document_id",
        nullable = false
    )
    Document document;
    /**
     * The index this column is in the associated document above.
     */
    @Column(nullable = false)
    int tableColumnIndex;

    public DocumentColumn() {
    }

    public DocumentColumn(DocumentColumnAppEntity documentColumnAppEntity, Document document, int tableColumnIndex) {
        this.documentColumnId = documentColumnAppEntity.getId();
        this.name = documentColumnAppEntity.getName();
        this.dataType = documentColumnAppEntity.getDataType();
        this.document = document;
        this.tableColumnIndex = tableColumnIndex;
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
