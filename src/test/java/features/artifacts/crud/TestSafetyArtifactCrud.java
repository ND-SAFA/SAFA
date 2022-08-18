package features.artifacts.crud;

import java.util.HashMap;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.SafetyCaseType;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;

import features.artifacts.base.AbstractArtifactCrudTest;

public class TestSafetyArtifactCrud extends AbstractArtifactCrudTest {
    @Override
    protected ArtifactAppEntity getStartingArtifact() {
        ArtifactAppEntity artifact = new ArtifactAppEntity("",
            DocumentType.SAFETY_CASE.toString(),
            "RE-20",
            "summary",
            "body",
            DocumentType.SAFETY_CASE,
            new HashMap<>()
        );
        artifact.setSafetyCaseType(SafetyCaseType.SOLUTION);
        return artifact;
    }

    @Override
    protected void modifyArtifact(ArtifactAppEntity artifact) {
        artifact.setSafetyCaseType(SafetyCaseType.CONTEXT);
    }
}
