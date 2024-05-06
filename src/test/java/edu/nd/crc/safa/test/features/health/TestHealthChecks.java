package edu.nd.crc.safa.test.features.health;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.comments.entities.dtos.ArtifactCommentResponseDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.ArtifactCommentDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.CommentDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.MultiArtifactCommentDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.UndefinedConceptCommentDTO;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentStatus;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentType;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.generation.common.GenerationLink;
import edu.nd.crc.safa.features.health.HealthConstants;
import edu.nd.crc.safa.features.health.entities.ConceptMatchDTO;
import edu.nd.crc.safa.features.health.entities.HealthResponseDTO;
import edu.nd.crc.safa.features.health.entities.gen.GenConceptResponse;
import edu.nd.crc.safa.features.health.entities.gen.GenContradiction;
import edu.nd.crc.safa.features.health.entities.gen.GenHealthResponse;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.features.generation.GenerationalTest;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

import org.junit.jupiter.api.Test;

class TestHealthChecks extends GenerationalTest {
    private static final int C1_LOC = 4;
    private static final int MULTI_LOC = 20;
    private static final String TARGET_NAME = "Target";
    private static final String UNDEFINED_CONCEPT_DEF = "Undefined concept.";
    private static final String CONTRADICTION_ID = "C4";
    private static final String CONTRADICTION_MSG = "this is a contradiction";

    /**
     * Direct matches: C1
     * MultiMatches: C2 + C3
     * PredictedMatches: C4
     * UndefinedEntities: U1
     * Contradiction:
     */

    @Test
    void testHealthChecks() throws Exception {
        ProjectVersion projectVersion = rootBuilder.actions(a -> a.createProjectWithVersion(getCurrentUser())).get();
        UUID artifactId = createProjectArtifacts(projectVersion);
        ArtifactAppEntity targetArtifact = new ArtifactAppEntity();
        targetArtifact.setId(artifactId);


        List<Artifact> projectArtifacts =
            getServiceProvider().getArtifactRepository().getProjectArtifacts(projectVersion.getProject());
        Map<UUID, Artifact> artifactLookup = ProjectDataStructures.createEntityLookup(projectArtifacts,
            Artifact::getArtifactId);

        mockHealthResponse();

        HealthResponseDTO healthResponseDTO = getServiceProvider()
            .getHealthService()
            .performArtifactHealthChecks(projectVersion, targetArtifact);

        List<CommentDTO> healthChecks = healthResponseDTO.getHealthChecks();
        UUID versionId = projectVersion.getVersionId();

        verifyDirectMatches(healthChecks, versionId, artifactLookup);
        verifyPredictedMatches(healthChecks, versionId, artifactLookup);
        verifyMultiMatches(healthChecks, versionId);
        verifyUndefinedMatches(healthChecks, versionId);
        verifyContradiction(healthChecks, versionId);

        ArtifactCommentResponseDTO artifactComments =
            getServiceProvider().getCommentRetrievalService().getArtifactComments(artifactId);
        assertThat(artifactComments.getComments().size()).isEqualTo(0);
        assertThat(artifactComments.getFlags().size()).isEqualTo(0);
        assertThat(artifactComments.getHealthChecks().size()).isEqualTo(5);

        healthChecks = artifactComments.getHealthChecks();

        verifyDirectMatches(healthChecks, versionId, artifactLookup);
        verifyPredictedMatches(healthChecks, versionId, artifactLookup);
        verifyMultiMatches(healthChecks, versionId);
        verifyUndefinedMatches(healthChecks, versionId);
        verifyContradiction(healthChecks, versionId);
    }

    private void verifyContradiction(List<CommentDTO> healthChecks, UUID versionId) {
        MultiArtifactCommentDTO comment = filterType(healthChecks, CommentType.CONTRADICTION, MultiArtifactCommentDTO.class);
        verifyCommentContent(versionId, comment, CONTRADICTION_MSG);
        assertThat(comment.getArtifactIds().size()).isEqualTo(1);
    }

    private void verifyUndefinedMatches(List<CommentDTO> healthChecks, UUID versionId) {
        UndefinedConceptCommentDTO comment = filterType(healthChecks, CommentType.UNDEFINED_CONCEPT, UndefinedConceptCommentDTO.class);
        verifyCommentContent(versionId, comment, "undefined");
        assertThat(comment.getUndefinedConcept()).contains("U1");
        assertThat(comment.getUndefinedConcept()).contains(UNDEFINED_CONCEPT_DEF);
    }

    private void verifyDirectMatches(List<CommentDTO> healthChecks,
                                     UUID versionId,
                                     Map<UUID, Artifact> artifactLookup) {
        ArtifactCommentDTO comment = filterType(healthChecks, CommentType.CITED_CONCEPT, ArtifactCommentDTO.class);
        verifyCommentContent(versionId, comment, "cited");
        assertConceptReference(comment, artifactLookup);
    }

    public void verifyPredictedMatches(List<CommentDTO> healthChecks,
                                       UUID versionId,
                                       Map<UUID, Artifact> artifactLookup) {
        ArtifactCommentDTO comment = filterType(healthChecks, CommentType.PREDICTED_CONCEPT, ArtifactCommentDTO.class);
        verifyCommentContent(versionId, comment, "predicted");
        assertConceptReference(comment, artifactLookup);
    }

    private void verifyMultiMatches(List<CommentDTO> healthChecks, UUID versionId) {
        MultiArtifactCommentDTO comment = filterType(healthChecks, CommentType.MULTI_MATCHED_CONCEPT,
            MultiArtifactCommentDTO.class);
        verifyCommentContent(versionId, comment, "multiple");
        assertThat(comment.getArtifactIds().size()).isEqualTo(2);
    }

    /**
     * Utility Methods
     */
    private void verifyCommentContent(UUID versionId, CommentDTO comment, String content) {
        assertThat(comment.getContent()).isNotNull().isNotEmpty().contains(content);
        assertThat(comment.getUserId()).isNull();
        assertThat(comment.getVersionId()).isEqualTo(versionId);
        assertThat(comment.getStatus()).isEqualTo(CommentStatus.ACTIVE);
        assertThat(comment.getTimeCreated()).isNotNull();
        assertThat(comment.getTimeUpdated()).isNotNull();
    }

    private void assertConceptReference(ArtifactCommentDTO comment, Map<UUID, Artifact> artifactLookup) {
        UUID conceptId = comment.getConceptCommentId();
        assertThat(artifactLookup.containsKey(conceptId)).isTrue();
        Artifact artifact = artifactLookup.get(conceptId);
        assertThat(artifact.getType().getName()).isEqualTo(HealthConstants.CONCEPT_TYPE);
    }

    public void mockHealthResponse() {
        GenHealthResponse genResponse = new GenHealthResponse();

        GenConceptResponse genConceptResponse = new GenConceptResponse();
        genConceptResponse.setMatches(List.of(new ConceptMatchDTO("C1", C1_LOC)));
        genConceptResponse.setMultiMatches(getTestMultiMatchMap());
        genConceptResponse.setPredictedMatches(List.of(asLink("C4")));
        genConceptResponse.setUndefinedEntities(List.of(asArtifact("U1")));

        GenContradiction genContradiction = new GenContradiction();
        genContradiction.setConflictingIds(List.of(CONTRADICTION_ID));
        genContradiction.setExplanation(CONTRADICTION_MSG);

        genResponse.setConceptMatches(genConceptResponse);
        genResponse.setContradictions(genContradiction);

        getServer().setJobResponse(genResponse);
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
        multiMatchMap.put(MULTI_LOC,
            List.of(new ConceptMatchDTO("C2", MULTI_LOC), new ConceptMatchDTO("C3", MULTI_LOC))
        );
        return multiMatchMap;
    }

    private UUID createProjectArtifacts(ProjectVersion projectVersion) {
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

    private <T extends CommentDTO> T filterType(List<CommentDTO> comments,
                                                CommentType commentType,
                                                Class<T> classType) {
        List<T> query = filterType(comments, commentType, classType, 1);
        assertThat(query.size()).isEqualTo(1);
        return query.get(0);
    }

    private <T extends CommentDTO> List<T> filterType(List<CommentDTO> comments,
                                                      CommentType commentType,
                                                      Class<T> classType,
                                                      int size) {
        List<T> items = comments
            .stream()
            .filter(c -> c.getType().equals(commentType))
            .map(comment -> {
                if (classType.isInstance(comment)) {
                    return classType.cast(comment);
                } else {
                    // Handle the case where the comment is not of the desired type
                    // For example, you might return null or throw an exception
                    return null;
                }
            })
            .filter(Objects::nonNull) // Filter out any null elements
            .toList();
        assertThat(items.size()).isEqualTo(size);
        return items;
    }
}
