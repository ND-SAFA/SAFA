package edu.nd.crc.safa.server.entities.api;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.Project;

public class DocumentAppEntity extends Document {

    List<String> artifactIds;

    public DocumentAppEntity() {
        super();
        this.artifactIds = new ArrayList<>();
    }

    public DocumentAppEntity(Document document,
                             List<String> artifactIds) {
        super(document);
        this.artifactIds = artifactIds;
    }

    public DocumentAppEntity(Project project,
                             List<String> artifactIds,
                             String name,
                             String description,
                             DocumentType type) {
        super(project, name, description, type);
        this.artifactIds = artifactIds;
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
