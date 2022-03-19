package edu.nd.crc.safa.server.entities.app;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.server.entities.db.Document;

public class DocumentAppEntity extends Document {

    List<String> artifactIds;
    List<DocumentColumnAppEntity> columns;

    public DocumentAppEntity() {
        super();
        this.artifactIds = new ArrayList<>();
    }

    public DocumentAppEntity(Document document,
                             List<String> artifactIds) {
        super(document);
        this.artifactIds = artifactIds;
    }

    public DocumentAppEntity(Document document,
                             List<String> artifactIds,
                             List<DocumentColumnAppEntity> columns) {
        super(document);
        this.artifactIds = artifactIds;
        this.columns = columns;
    }

    public List<DocumentColumnAppEntity> getColumns() {
        return columns;
    }

    public void setColumns(List<DocumentColumnAppEntity> columns) {
        this.columns = columns;
    }

    public Document toDocument() {
        return new Document(this);
    }

    public List<String> getArtifactIds() {
        return artifactIds;
    }

    public void setArtifactIds(List<String> artifactIds) {
        this.artifactIds = artifactIds;
    }
}
