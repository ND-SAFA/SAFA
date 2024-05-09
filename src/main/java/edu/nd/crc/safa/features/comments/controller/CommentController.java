package edu.nd.crc.safa.features.comments.controller;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.comments.CommentService;
import edu.nd.crc.safa.features.comments.entities.dtos.ArtifactCommentResponseDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.CommentCreateRequestDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.CommentUpdateRequestDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.CommentDTO;
import edu.nd.crc.safa.features.comments.entities.persistent.Comment;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentType;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CommentController extends BaseController {
    private static final List<CommentType> ACCEPTED_TYPES = List.of(CommentType.CONVERSATION, CommentType.FLAG);

    public CommentController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Creates new comment on artifact.
     *
     * @param artifactId              Artifact ID to create comment on.
     * @param commentCreateRequestDTO Contains content and type of comment to create.
     * @return DTO of created comment.
     */
    @PostMapping(AppRoutes.Comments.COMMENT_CREATE)
    public CommentDTO createComment(@PathVariable UUID artifactId,
                                    @RequestBody @Valid CommentCreateRequestDTO commentCreateRequestDTO) {
        SafaUser currentUser = getCurrentUser();
        ProjectVersion projectVersion = getResourceBuilder()
            .fetchVersion(commentCreateRequestDTO.getVersionId())
            .asUser(currentUser)
            .withPermission(ProjectPermission.EDIT)
            .get();


        if (!ACCEPTED_TYPES.contains(commentCreateRequestDTO.getType())) {
            throw new SafaError(String.format("Expected comment type to be one of: %s.", ACCEPTED_TYPES));
        }

        return this.getServiceProvider().getCommentService().createConversationComment(
            commentCreateRequestDTO,
            artifactId,
            currentUser,
            projectVersion
        );
    }

    /**
     * Updates content of comment.
     *
     * @param commentUpdateRequestDTO Contains new content of comment.
     * @param commentId               ID of comment to update.
     * @return DTO of updated comment.
     */
    @PutMapping(AppRoutes.Comments.COMMENT_UPDATE_CONTENT)
    public CommentDTO updateCommentContent(@RequestBody CommentUpdateRequestDTO commentUpdateRequestDTO,
                                           @PathVariable UUID commentId) {
        SafaUser currentUser = getCurrentUser();
        CommentService commentService = this.getServiceProvider().getCommentService();
        Comment comment = commentService.getCommentById(commentId);

        if (!ACCEPTED_TYPES.contains(comment.getType())) {
            throw new SafaError(String.format("Expected comment type to be one of: %s.", ACCEPTED_TYPES));
        }

        return commentService.updateCommentContent(currentUser, comment, commentUpdateRequestDTO.getContent());
    }

    /**
     * Marks a comment as resolved.
     *
     * @param commentId ID of comment to mark as resolved.
     * @return The comment with updated content.
     */
    @PutMapping(AppRoutes.Comments.COMMENT_RESOLVE)
    public CommentDTO resolveComment(@PathVariable UUID commentId) {
        SafaUser currentUser = getCurrentUser();
        CommentService commentService = this.getServiceProvider().getCommentService();
        Comment comment = commentService.getCommentById(commentId);
        getResourceBuilder()
            .withVersion(comment.getVersion())
            .asUser(currentUser)
            .withPermission(ProjectPermission.EDIT);
        return commentService.toggleResolve(commentId);
    }

    /**
     * Deletes comment with given ID.
     *
     * @param commentId ID of comment to delete.
     */
    @DeleteMapping(AppRoutes.Comments.COMMENT_DELETE)
    public void deleteComment(@PathVariable UUID commentId) {
        SafaUser currentUser = getCurrentUser();
        getServiceProvider().getCommentService().deleteComment(currentUser, commentId);
    }

    /**
     * Retrieves comments for artifact.
     *
     * @param artifactId ID of artifact whose comments are retrieved.
     * @return Collection of comments on artifact.
     */
    @GetMapping(AppRoutes.Comments.COMMENT_GET)
    public ArtifactCommentResponseDTO getArtifactComments(@PathVariable UUID artifactId) {
        return getServiceProvider().getCommentRetrievalService().getArtifactComments(artifactId);
    }
}
