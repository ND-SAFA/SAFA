package features.artifacts.crud;

import java.util.HashMap;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.FTAType;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;

import features.artifacts.base.AbstractArtifactCrudTest;

public class TestFTACrud extends AbstractArtifactCrudTest {
    @Override
    protected ArtifactAppEntity getStartingArtifact() {
        ArtifactAppEntity artifact = new ArtifactAppEntity("",
            DocumentType.FMEA.toString(),
            "RE-20",
            "summary",
            "body",
            DocumentType.FTA,
            new HashMap<>()
        );
        artifact.setLogicType(FTAType.AND);
        return artifact;
    }

    @Override
    protected void modifyArtifact(ArtifactAppEntity artifact) {
        artifact.setLogicType(FTAType.OR);
    }
}
