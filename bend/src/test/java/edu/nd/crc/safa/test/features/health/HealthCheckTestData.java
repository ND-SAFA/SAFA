package edu.nd.crc.safa.test.features.health;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.generation.common.GenerationLink;
import edu.nd.crc.safa.features.health.HealthConstants;
import edu.nd.crc.safa.features.health.entities.ConceptMatchDTO;
import edu.nd.crc.safa.features.health.entities.gen.GenContradiction;
import edu.nd.crc.safa.features.health.entities.gen.GenHealthResponse;
import edu.nd.crc.safa.features.health.entities.gen.GenUndefinedEntity;
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
    public static final String UNDEFINED_CONCEPT_DEFINITION = "example definition";
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
        genResponse.setDirectMatches(List.of(new ConceptMatchDTO(TARGET_NAME, "C1", C1_START_LOC, C1_END_LOC)));
        genResponse.setMultiMatches(getTestMultiMatchMap());
        genResponse.setPredictedMatches(List.of(asConceptLink("C4")));
        genResponse.setUndefinedConcepts(List.of(
            new GenUndefinedEntity(
                List.of(TARGET_NAME),
                "U1",
                UNDEFINED_CONCEPT_DEFINITION
            )
        ));

        GenContradiction genContradiction = new GenContradiction();
        genContradiction.setConflictingIds(List.of(TARGET_NAME));
        genContradiction.setExplanation(HealthCheckTestVerifier.CONTRADICTION_MSG);
        genResponse.setContradictions(List.of(genContradiction));
        return genResponse;
    }

    private GenerationLink asConceptLink(String conceptId) {
        GenerationLink link = new GenerationLink();
        link.setSource(TARGET_NAME);
        link.setTarget(conceptId);
        return link;
    }

    private Map<String, Map<Integer, List<ConceptMatchDTO>>> getTestMultiMatchMap() {
        Map<Integer, List<ConceptMatchDTO>> artifactMultiMatch = new HashMap<>();
        artifactMultiMatch.put(MULTI_START_LOC,
            List.of(
                new ConceptMatchDTO(TARGET_NAME, "C2", MULTI_START_LOC, MULTI_END_LOC),
                new ConceptMatchDTO(TARGET_NAME, "C3", MULTI_START_LOC, MULTI_END_LOC)
            )
        );
        Map<String, Map<Integer, List<ConceptMatchDTO>>> multiMatch = new HashMap<>();
        multiMatch.put(TARGET_NAME, artifactMultiMatch);
        return multiMatch;
    }

}
