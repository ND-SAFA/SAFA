package edu.nd.crc.safa.server.entities.app.documents;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.layout.LayoutPosition;
import edu.nd.crc.safa.server.entities.db.Document;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class DocumentAppEntity extends Document {
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
}
