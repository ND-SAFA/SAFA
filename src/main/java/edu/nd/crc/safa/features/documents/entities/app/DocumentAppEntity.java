package edu.nd.crc.safa.features.documents.entities.app;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class DocumentAppEntity extends Document implements IAppEntity {
    private List<String> artifactIds = new ArrayList<>();
    private List<DocumentColumnAppEntity> columns = new ArrayList<>();
    private Map<String, LayoutPosition> layout = new HashMap<>();

    public DocumentAppEntity(Document document,
                             List<String> artifactIds,
                             Map<String, LayoutPosition> layout) {
        super(document);
        this.artifactIds = artifactIds;
        this.columns = new ArrayList<>();
        this.layout = layout;
    }

    public Document toDocument() {
        return new Document(this);
    }

    @Override
    public String getBaseEntityId() {
        return this.getDocumentId().toString();
    }

    @Override
    public void setBaseEntityId(String id) {
        this.setDocumentId(UUID.fromString(id));
    }
}
