package features.artifacts.crud;

import java.util.HashMap;
import java.util.Map;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.TextNode;
import features.artifacts.base.AbstractArtifactCrudTest;

public class TestFMEACrud extends AbstractArtifactCrudTest {
    @Override
    protected ArtifactAppEntity getStartingArtifact() {
        Map<String, JsonNode> customFields = new HashMap<>();
        customFields.put("key", TextNode.valueOf("value"));
        return new ArtifactAppEntity(null,
            DocumentType.FMEA.toString(),
            "RE-20",
            "summary",
            "body",
            DocumentType.FMEA,
            customFields
        );
    }

    @Override
    protected void modifyArtifact(ArtifactAppEntity artifact) {
        Map<String, JsonNode> customFields = artifact.getAttributes();
        customFields.put("key", TextNode.valueOf("newValue"));
    }
}
