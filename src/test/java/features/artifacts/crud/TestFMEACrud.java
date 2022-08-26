package features.artifacts.crud;

import java.util.HashMap;
import java.util.Map;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;

import features.artifacts.base.AbstractArtifactCrudTest;

public class TestFMEACrud extends AbstractArtifactCrudTest {
    @Override
    protected ArtifactAppEntity getStartingArtifact() {
        Map<String, String> customFields = new HashMap<>();
        customFields.put("key", "value");
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
        Map<String, String> customFields = artifact.getCustomFields();
        customFields.put("key", "newValue");
    }
}
