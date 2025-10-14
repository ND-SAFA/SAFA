package edu.nd.crc.safa.test.features.artifacts.crud;

import java.util.HashMap;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.test.features.artifacts.base.AbstractArtifactCrudTest;

public class TestArtifactCrud extends AbstractArtifactCrudTest {
    @Override
    protected ArtifactAppEntity getStartingArtifact() {
        return new ArtifactAppEntity(null,
            "Requirements",
            "RE-20",
            "summary",
            "body",
            new HashMap<>()
        );
    }

    @Override
    protected void modifyArtifact(ArtifactAppEntity artifact) {
        artifact.setSummary("new summary");
    }
}
