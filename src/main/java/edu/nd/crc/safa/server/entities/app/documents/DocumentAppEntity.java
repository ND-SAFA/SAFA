package edu.nd.crc.safa.server.entities.app.documents;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.server.entities.db.Document;

import lombok.Data;

@Data
public class DocumentAppEntity extends Document {

    List<String> artifactIds;
    List<DocumentColumnAppEntity> columns;

    public DocumentAppEntity() {
        super();
        this.artifactIds = new ArrayList<>();
        this.columns = new ArrayList<>();
    }

    public DocumentAppEntity(Document document,
                             List<String> artifactIds) {
        super(document);
        this.artifactIds = artifactIds;
        this.columns = new ArrayList<>();
    }

    public Document toDocument() {
        return new Document(this);
    }
}
