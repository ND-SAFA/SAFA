package features.artifacts.crud;

import java.util.HashMap;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;

import features.artifacts.base.AbstractArtifactCrudTest;

public class TestArtifactCrud extends AbstractArtifactCrudTest {
    @Override
    protected ArtifactAppEntity getStartingArtifact() {
        return new ArtifactAppEntity("",
            "Requirements",
            "RE-20",
            "summary",
            "body",
            DocumentType.ARTIFACT_TREE,
            new HashMap<>()
        );
    }

    @Override
    protected void modifyArtifact(ArtifactAppEntity artifact) {
        artifact.setSummary("new summary");
    }
}
