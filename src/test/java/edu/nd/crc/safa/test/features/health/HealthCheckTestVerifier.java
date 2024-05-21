package edu.nd.crc.safa.test.features.health;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

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
import edu.nd.crc.safa.features.health.HealthConstants;
import edu.nd.crc.safa.features.health.entities.HealthResponseDTO;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

public class HealthCheckTestVerifier {
    public static final String CONTRADICTION_MSG = "this is a contradiction";
    private final ProjectVersion projectVersion;
    private final Map<UUID, Artifact> artifactLookup;

    public HealthCheckTestVerifier(ProjectVersion projectVersion,
                                   List<Artifact> projectArtifacts) {
        this.projectVersion = projectVersion;
        this.artifactLookup = ProjectDataStructures.createEntityLookup(projectArtifacts,
            Artifact::getArtifactId);
    }

    public void verifyHealthResponse(HealthResponseDTO healthResponseDTO) {
        List<CommentDTO> healthChecks = healthResponseDTO.getHealthChecks();
        verifyCommentDTOS(healthChecks);
    }

    public void verifyArtifactComments(ArtifactCommentResponseDTO artifactComments) {
        assertThat(artifactComments.getComments().size()).isEqualTo(0);
        assertThat(artifactComments.getFlags().size()).isEqualTo(0);
        assertThat(artifactComments.getHealthChecks().size()).isEqualTo(5);

        List<CommentDTO> healthChecks = artifactComments.getHealthChecks();
        verifyCommentDTOS(healthChecks);
    }

    public void verifyCommentDTOS(List<CommentDTO> healthChecks) {
        UUID versionId = projectVersion.getVersionId();
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

    private void verifyCommentContent(UUID versionId, CommentDTO comment, String content) {
        assertThat(comment.getContent()).isNotNull().isNotEmpty().contains(content);
        assertThat(comment.getUserId()).isNull();
        assertThat(comment.getVersionId()).isEqualTo(versionId);
        assertThat(comment.getStatus()).isEqualTo(CommentStatus.ACTIVE);
        assertThat(comment.getCreatedAt()).isNotNull();
        assertThat(comment.getUpdatedAt()).isNotNull();
    }

    private void assertConceptReference(ArtifactCommentDTO comment, Map<UUID, Artifact> artifactLookup) {
        UUID conceptId = comment.getConceptArtifactId();
        assertThat(artifactLookup.containsKey(conceptId)).isTrue();
        Artifact artifact = artifactLookup.get(conceptId);
        assertThat(artifact.getType().getName()).isEqualTo(HealthConstants.CONCEPT_TYPE);
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
