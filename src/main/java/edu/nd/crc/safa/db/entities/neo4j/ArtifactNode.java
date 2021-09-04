package edu.nd.crc.safa.db.entities.neo4j;

import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Property;

@Node("Artifact")
public class ArtifactNode {
    @Id
    private final String id; // TODO: Change to UUID

    @Property("type")
    private final String type;

    @Property("data")
    private final String data;

    public ArtifactNode(String id, String type, String data) {
        this.id = id;
        this.type = type;
        this.data = data;
    }

    public String getId() {
        return this.id;
    }

    public String getType() {
        return this.type;
    }

    public String getData() {
        return this.data;
    }
}
