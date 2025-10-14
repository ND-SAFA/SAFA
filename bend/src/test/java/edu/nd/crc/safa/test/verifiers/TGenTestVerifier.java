package edu.nd.crc.safa.test.verifiers;

import static org.junit.jupiter.api.Assertions.assertEquals;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.test.features.generation.GenerationalTest;
import edu.nd.crc.safa.test.services.GenTestService;

public class TGenTestVerifier {
    public static void verifyCodeHasSummaries(GenerationalTest test) {
        test
            .getProject()
            .getArtifacts()
            .stream()
            .filter(ArtifactAppEntity::isCode)
            .forEach(a -> {
                String artifactSummary = GenTestService.createArtifactSummary(a);
                assertEquals(artifactSummary, a.getSummary());
            });
    }
}
