package edu.nd.crc.safa.features.comments;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.comments.entities.dtos.CommentCreateRequestDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.CommentDTO;
import edu.nd.crc.safa.features.comments.entities.persistent.Comment;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentStatus;
import edu.nd.crc.safa.features.comments.repositories.CommentRepository;
import edu.nd.crc.safa.features.comments.services.CommentRetrievalService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.jetbrains.annotations.NotNull;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class CommentService {
    private CommentRetrievalService commentRetrievalService;
    private CommentRepository commentRepository;
    private ArtifactService artifactService;

    /**
     * Creates comment from request DTO.
     *
     * @param commentCreateRequestDTO Request containing content, type, version id, and artifact id.
     * @param artifactId              ID of artifact to create comment on.
     * @param author                  User who wrote the comment.
     * @param projectVersion          Project version this comment was created in.
     * @return DTO.
     */
    @NotNull
    public CommentDTO createConversationComment(CommentCreateRequestDTO commentCreateRequestDTO,
                                                UUID artifactId,
                                                SafaUser author,
                                                ProjectVersion projectVersion) {
        Artifact artifact = artifactService.findById(artifactId);

        Comment comment = new Comment();
        comment.setContent(commentCreateRequestDTO.getContent());
        comment.setStatus(CommentStatus.ACTIVE);
        comment.setType(commentCreateRequestDTO.getType());
        comment.setAuthor(author);
        comment.setVersion(projectVersion);
        comment.setArtifact(artifact);

        comment = commentRepository.save(comment);

        return CommentDTO.fromComment(comment);
    }

    /**
     * Updates the content of the comment.
     *
     * @param user    The user attempting to udpate comment.
     * @param comment The comment to update.
     * @param content The new content.
     * @return Updated DTO.
     */
    @NotNull
    public CommentDTO updateCommentContent(SafaUser user, Comment comment, String content) {
        verifyCommentAuthor(user, comment, "Only author of comment is able to edit content.");
        comment.setContent(content);
        comment = commentRepository.save(comment);
        return CommentDTO.fromComment(comment);
    }

    /**
     * Deletes comment with ID.
     *
     * @param user      The user attempting to delete comment.
     * @param commentId ID of comment to delete.
     */
    public void deleteComment(SafaUser user, UUID commentId) {
        Comment comment = getCommentById(commentId);
        verifyCommentAuthor(user, comment, "Only comment author is able to delete comment.");
        commentRepository.delete(comment);
    }

    /**
     * Marks comment as resolved.
     *
     * @param commentId Id of comment to resolve.
     * @return CommentDTO after comment saved.
     */
    public CommentDTO toggleResolve(UUID commentId) {
        Comment comment = getCommentById(commentId);
        comment.setStatus(comment.getStatus().toggle());
        this.commentRepository.save(comment);
        return commentRetrievalService.retrieveCommentDTO(comment);
    }

    /**
     * Returns comment with given ID.
     *
     * @param commentId ID of comment to retrieve.
     * @return Comment.
     */
    @NotNull
    public Comment getCommentById(UUID commentId) {
        Optional<Comment> commentOptional = commentRepository.findById(commentId);
        if (commentOptional.isEmpty()) {
            throw new SafaError("Unable to find comment with given ID.");
        }
        return commentOptional.get();
    }

    /**
     * Verifies that given user is author of comment.
     *
     * @param user    The user to check against author of comment.
     * @param comment The comment to verify.
     * @param message The message in error if user is not author.
     */
    public void verifyCommentAuthor(SafaUser user, Comment comment, String message) {
        if (!comment.isAuthor(user)) {
            throw new SafaError(message);
        }
    }
}
