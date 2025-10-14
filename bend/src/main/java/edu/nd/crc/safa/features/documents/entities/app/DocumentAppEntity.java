package edu.nd.crc.safa.features.documents.entities.app;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DocumentAppEntity implements IAppEntity {
    private UUID documentId = null;
    @NotEmpty
    private String name;
    @NotNull
    private String description;
    @NotNull
    private List<UUID> artifactIds = new ArrayList<>();
    private Map<UUID, LayoutPosition> layout = new HashMap<>();

    public DocumentAppEntity(Document document,
                             List<UUID> artifactIds,
                             Map<UUID, LayoutPosition> layout) {
        this.documentId = document.getDocumentId();
        this.name = document.getName();
        this.description = document.getDescription();
        this.artifactIds = artifactIds;
        this.layout = layout;
    }

    public Document toDocument() {
        return new Document(
            this.documentId,
            null,
            this.name,
            this.description);
    }

    @Override
    public UUID getId() {
        return this.getDocumentId();
    }

    @Override
    public void setId(UUID id) {
        this.documentId = id;
    }
}
