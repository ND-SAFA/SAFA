package edu.nd.crc.safa.features.documents.entities.app;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DocumentAppEntity implements IAppEntity {
    private String documentId;
    private DocumentType documentType;
    private String name;
    private String description;
    private List<String> artifactIds = new ArrayList<>();
    private List<DocumentColumnAppEntity> columns = new ArrayList<>();
    private Map<String, LayoutPosition> layout = new HashMap<>();

    public DocumentAppEntity(Document document,
                             List<String> artifactIds,
                             Map<String, LayoutPosition> layout) {
        this.documentId = document.getDocumentId().toString();
        this.documentType = document.getType();
        this.name = document.getName();
        this.description = document.getDescription();
        this.artifactIds = artifactIds;
        this.columns = new ArrayList<>();
        this.layout = layout;
    }

    public Document toDocument() {
        UUID documentId = this.documentId.isEmpty() ? null : UUID.fromString(this.documentId);
        return new Document(
            documentId,
            null,
            this.documentType,
            this.name,
            this.description);
    }

    @Override
    public String getBaseEntityId() {
        return this.getDocumentId();
    }

    @Override
    public void setBaseEntityId(String id) {
        this.setDocumentId(id);
    }
}
