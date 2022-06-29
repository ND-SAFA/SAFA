package edu.nd.crc.safa.server.entities.app.documents;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.layout.LayoutPosition;
import edu.nd.crc.safa.server.entities.db.Document;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class DocumentAppEntity extends Document {

    List<String> artifactIds = new ArrayList<>();
    List<DocumentColumnAppEntity> columns = new ArrayList<>();
    @JsonProperty(access = JsonProperty.Access.READ_ONLY)
    Map<String, LayoutPosition> layout = new Hashtable<>();

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
