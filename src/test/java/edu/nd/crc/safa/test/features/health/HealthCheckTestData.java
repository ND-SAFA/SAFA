package edu.nd.crc.safa.test.features.health;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.generation.common.GenerationLink;
import edu.nd.crc.safa.features.health.HealthConstants;
import edu.nd.crc.safa.features.health.entities.ConceptMatchDTO;
import edu.nd.crc.safa.features.health.entities.gen.GenConceptResponse;
import edu.nd.crc.safa.features.health.entities.gen.GenContradiction;
import edu.nd.crc.safa.features.health.entities.gen.GenHealthResponse;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.services.builders.DbEntityBuilder;

/**
 * Test Data Specification:
 * Direct matches: C1
 * MultiMatches: C2 + C3
 * PredictedMatches: C4
 * UndefinedEntities: U1
 * Contradiction with C1
 */
public class HealthCheckTestData {
    private static final int C1_START_LOC = 4;
    private static final int C1_END_LOC = C1_START_LOC + 3;
    private static final int MULTI_START_LOC = 20;
    private static final int MULTI_END_LOC = 20 + 3;
    private static final String TARGET_NAME = "Target";
    private static final String UNDEFINED_CONCEPT_DEF = "Undefined concept.";
    private static final String CONTRADICTION_ID = "C4";

    public static int N_MULTI_MATCHES = 2;

    public UUID createProjectArtifacts(ProjectVersion projectVersion, DbEntityBuilder dbEntityBuilder) {
        String projectName = projectVersion.getProject().getName();
        dbEntityBuilder.setVersion(projectVersion);
        dbEntityBuilder.newType(projectName, HealthConstants.CONCEPT_TYPE).newType(projectName, "Requirement");
        for (int i = 1; i <= 5; i++) {
            String artifactName = String.format("C%s", i);
            dbEntityBuilder.newArtifactAndBody(projectName,
                HealthConstants.CONCEPT_TYPE, artifactName, "", "");
        }
        return dbEntityBuilder.newArtifactAndBody(projectVersion.getProject().getName(),
                "Requirement", "Target", "", "")
            .getArtifact(projectName, TARGET_NAME)
            .getArtifactId();
    }

    /**
     * Creates mock GEN health response
     *
     * @return
     */
    public GenHealthResponse createMockGenHealthResponse() {
        GenHealthResponse genResponse = new GenHealthResponse();

        GenConceptResponse genConceptResponse = new GenConceptResponse();
        genConceptResponse.setMatches(List.of(new ConceptMatchDTO("C1", C1_START_LOC, C1_END_LOC)));
        genConceptResponse.setMultiMatches(getTestMultiMatchMap());
        genConceptResponse.setPredictedMatches(List.of(asLink("C4")));
        genConceptResponse.setUndefinedEntities(List.of(asArtifact("U1")));

        GenContradiction genContradiction = new GenContradiction();
        genContradiction.setConflictingIds(List.of(CONTRADICTION_ID));
        genContradiction.setExplanation(HealthCheckTestVerifier.CONTRADICTION_MSG);

        genResponse.setConceptMatches(genConceptResponse);
        genResponse.setContradictions(genContradiction);
        return genResponse;
    }

    private GenerationLink asLink(String aId) {
        GenerationLink link = new GenerationLink();
        link.setTarget(aId);
        link.setSource("test entity");
        return link;
    }

    private GenerationArtifact asArtifact(String aId) {
        GenerationArtifact artifact = new GenerationArtifact();
        artifact.setId(aId);
        artifact.setContent(UNDEFINED_CONCEPT_DEF);
        return artifact;
    }

    private Map<Integer, List<ConceptMatchDTO>> getTestMultiMatchMap() {
        Map<Integer, List<ConceptMatchDTO>> multiMatchMap = new HashMap<>();
        multiMatchMap.put(MULTI_START_LOC,
            List.of(
                new ConceptMatchDTO("C2", MULTI_START_LOC, MULTI_END_LOC),
                new ConceptMatchDTO("C3", MULTI_START_LOC, MULTI_END_LOC)
            )
        );
        return multiMatchMap;
    }

}
