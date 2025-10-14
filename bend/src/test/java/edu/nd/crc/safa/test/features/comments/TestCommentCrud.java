package edu.nd.crc.safa.test.features.comments;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.comments.entities.dtos.ArtifactCommentResponseDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.CommentCreateRequestDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.CommentUpdateRequestDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.CommentDTO;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentStatus;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentType;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

class TestCommentCrud extends ApplicationBaseTest {

    /**
     * Creates new comment, updates its content, and finally deletes it.
     *
     * @throws Exception If HTTP error or parsing error occurs.
     */
    @Test
    void createComment() throws Exception {
        String commentContent = "this is the comment";
        String newContent = "this is the new content";
        CommentType commentType = CommentType.CONVERSATION;

        // Setup - Create Project, Version, and Artifact to comment on.
        SafaUser currentUser = getCurrentUser();
        ProjectVersion projectVersion = rootBuilder.actions(a -> a.createProjectWithVersion(currentUser)).get();
        ArtifactAppEntity artifactCreated = createArtifact(projectVersion);

        // Step - Verify no comments exists
        verifyEmptyComments(artifactCreated.getId());

        // Step -  Create comment
        CommentCreateRequestDTO request = new CommentCreateRequestDTO(
            commentContent, commentType, projectVersion.getId());
        CommentDTO commentCreated = SafaRequest
            .withRoute(AppRoutes.Comments.COMMENT_CREATE)
            .withArtifactId(artifactCreated.getId())
            .postWithJsonObject(request, CommentDTO.class);

        verifyCommentContent(commentCreated, commentContent, currentUser, projectVersion);

        // Step - Verify one comment exists with correct content.
        verifyArtifactComments(artifactCreated.getId(), List.of(commentContent));

        // Step - Update content of comment.
        CommentUpdateRequestDTO commentUpdateRequest = new CommentUpdateRequestDTO(newContent);
        CommentDTO commentUpdated = SafaRequest
            .withRoute(AppRoutes.Comments.COMMENT_UPDATE_CONTENT)
            .withCustomReplacement("commentId", commentCreated.getId())
            .putWithJsonObject(commentUpdateRequest, CommentDTO.class);
        verifyCommentContent(commentUpdated, newContent, currentUser, projectVersion);

        // Step - Verify one comment exists with new content.
        verifyArtifactComments(artifactCreated.getId(), List.of(newContent));

        // Step - Resolve comment.
        SafaRequest
            .withRoute(AppRoutes.Comments.COMMENT_RESOLVE)
            .withCustomReplacement("commentId", commentCreated.getId())
            .putWithJsonObject(new JSONObject());

        // Step - Verify resolution in status.
        ArtifactCommentResponseDTO resolveResponse = verifyArtifactComments(artifactCreated.getId(),
            List.of(newContent));
        assertThat(resolveResponse.getComments().get(0).getStatus()).isEqualTo(CommentStatus.RESOLVED);

        // Step - delete
        SafaRequest
            .withRoute(AppRoutes.Comments.COMMENT_DELETE)
            .withCustomReplacement("commentId", commentCreated.getId())
            .deleteWithJsonObject();

        // step - verify no comments exist.
        verifyEmptyComments(artifactCreated.getId());
    }

    /**
     * Verifies that content of comment.
     *
     * @param commentCreated The comment to verify.
     * @param content        Expected content of comment.
     * @param currentUser    Expected author of comment.
     * @param projectVersion Expected project version of comment.
     */
    private void verifyCommentContent(CommentDTO commentCreated,
                                      String content,
                                      SafaUser currentUser,
                                      ProjectVersion projectVersion) {
        assertThat(commentCreated.getId()).isNotNull();
        assertThat(commentCreated.getContent()).isEqualTo(content);
        assertThat(commentCreated.getUserId()).isEqualTo(currentUser.getEmail());
        assertThat(commentCreated.getVersionId()).isEqualTo(projectVersion.getId());
        assertThat(commentCreated.getStatus()).isEqualTo(CommentStatus.ACTIVE);
        assertThat(commentCreated.getType()).isEqualTo(CommentType.CONVERSATION);
        assertThat(commentCreated.getCreatedAt()).isNotNull();
        assertThat(commentCreated.getUpdatedAt()).isNotNull();
    }

    /**
     * Helper method for verifying that artifact contains no comments.
     *
     * @param artifactId ID of artifact to verify comments for.
     * @throws Exception If error occurs while getting comments.
     */
    private void verifyEmptyComments(UUID artifactId) throws Exception {
        verifyArtifactComments(artifactId, new ArrayList<>());
    }

    /**
     * Verify that artifact contains specified comment bodies.
     *
     * @param artifactId    ID of artifact whose comments are verified.
     * @param commentBodies Expect list of comment bodies in order expected to be found.
     * @throws Exception If error occurs while retrieving comments.
     */
    private ArtifactCommentResponseDTO verifyArtifactComments(UUID artifactId,
                                                              List<String> commentBodies) throws Exception {
        ArtifactCommentResponseDTO artifactComments = getArtifactComments(artifactId);
        assertThat(artifactComments.getComments().size()).isEqualTo(commentBodies.size());
        assertThat(artifactComments.getFlags().size()).isZero();
        assertThat(artifactComments.getHealthChecks().size()).isZero();
        for (int i = 0; i < commentBodies.size(); i++) {
            assertThat(artifactComments.getComments().get(i).getContent()).isEqualTo(commentBodies.get(i));
        }
        return artifactComments;
    }

    /**
     * Returns artifact comments.
     *
     * @param artifactId ID of artifact whose comments are retrieved.
     * @return Set of comments on artifacts.
     * @throws Exception
     */
    private ArtifactCommentResponseDTO getArtifactComments(UUID artifactId) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Comments.COMMENT_GET)
            .withArtifactId(artifactId)
            .getAsType(ArtifactCommentResponseDTO.class);
    }

    /**
     * Creates artifact to be commented on.
     *
     * @param projectVersion The version this artifact is created in.
     * @return DTO for artifact created.
     */
    private ArtifactAppEntity createArtifact(ProjectVersion projectVersion) {
        ArtifactAppEntity artifact = new ArtifactAppEntity();
        String artifactName = "RE-8";
        artifact.setName(artifactName);
        String artifactBody = "This is the body";
        artifact.setBody(artifactBody);
        String artifactType = "Requirement";
        artifact.setType(artifactType);
        return rootBuilder
            .actions(a -> a.commit(CommitBuilder
                .withVersion(projectVersion).withAddedArtifact(artifact))).get().getArtifact(ModificationType.ADDED, 0);
    }
}
