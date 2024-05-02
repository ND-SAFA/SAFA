package edu.nd.crc.safa.test.features.health;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.comments.entities.dtos.ArtifactCommentResponseDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.ArtifactCommentDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.CommentDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.MultiArtifactCommentDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.UndefinedConceptCommentDTO;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentStatus;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentType;
import edu.nd.crc.safa.features.health.ConceptMatchDTO;
import edu.nd.crc.safa.features.health.HealthConstants;
import edu.nd.crc.safa.features.health.HealthGenResponse;
import edu.nd.crc.safa.features.health.HealthResponse;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.features.generation.GenerationalTest;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

import org.junit.jupiter.api.Test;

class TestHealthGeneration extends GenerationalTest {
    private static final int C1_LOC = 4;
    private static final int MULTI_LOC = 20;
    private static final String TARGET_NAME = "Target";


    /**
     * Direct matches: C1
     * MultiMatches: C2 + C3
     * PredictedMatches: C4
     * UndefinedEntities: U1
     */

    @Test
    void testHealthChecks() throws Exception {
        ProjectVersion projectVersion = rootBuilder.actions(a -> a.createProjectWithVersion(getCurrentUser())).get();
        UUID artifactId = createProjectArtifacts(projectVersion);


        List<Artifact> projectArtifacts =
            getServiceProvider().getArtifactRepository().getProjectArtifacts(projectVersion.getProject());
        Map<UUID, Artifact> artifactLookup = ProjectDataStructures.createEntityLookup(projectArtifacts,
            Artifact::getArtifactId);

        mockHealthResponse();

        HealthResponse healthResponse = getServiceProvider()
            .getHealthService()
            .performArtifactHealthChecks(projectVersion, artifactId);

        List<CommentDTO> healthChecks = healthResponse.getHealthChecks();
        UUID versionId = projectVersion.getVersionId();

        verifyDirectMatches(healthChecks, versionId, artifactLookup);
        verifyPredictedMatches(healthChecks, versionId, artifactLookup);
        verifyMultiMatches(healthChecks, versionId);
        verifyUndefinedMatches(healthChecks, versionId);

        ArtifactCommentResponseDTO artifactComments =
            getServiceProvider().getCommentRetrievalService().getArtifactComments(artifactId);
        assertThat(artifactComments.getComments().size()).isEqualTo(0);
        assertThat(artifactComments.getFlags().size()).isEqualTo(0);
        assertThat(artifactComments.getHealthChecks().size()).isEqualTo(4);

        healthChecks = artifactComments.getHealthChecks();

        verifyDirectMatches(healthChecks, versionId, artifactLookup);
        verifyPredictedMatches(healthChecks, versionId, artifactLookup);
        verifyMultiMatches(healthChecks, versionId);
        verifyUndefinedMatches(healthChecks, versionId);
    }

    private void verifyUndefinedMatches(List<CommentDTO> healthChecks, UUID versionId) {
        UndefinedConceptCommentDTO comment = filterType(healthChecks, CommentType.UNDEFINED_CONCEPT, UndefinedConceptCommentDTO.class);
        verifyCommentContent(versionId, comment, "undefined");
        assertThat(comment.getUndefinedConcept()).isEqualTo("U1");
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
        HealthGenResponse genResponse = new HealthGenResponse();
        genResponse.setMatches(List.of(new ConceptMatchDTO("C1", C1_LOC)));
        genResponse.setMultiMatches(getTestMultiMatchMap());
        genResponse.setPredictedMatches(List.of("C4"));
        genResponse.setUndefinedEntities(List.of("U1"));
        getServer().setResponse(genResponse);
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
