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
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.jetbrains.annotations.NotNull;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class CommentService {
    private CommentRepository commentRepository;
    private ArtifactService artifactService;

    /**
     * Creates comment from request DTO.
     *
     * @param commentCreateRequestDTO Request containing content, type, version id, and artifact id.
     * @param author                  User who wrote the comment.
     * @param projectVersion          Project version this comment was created in.
     * @return DTO.
     */
    public CommentDTO createConversationComment(CommentCreateRequestDTO commentCreateRequestDTO,
                                                SafaUser author,
                                                ProjectVersion projectVersion) {
        Artifact artifact = artifactService.findById(commentCreateRequestDTO.getArtifactId());

        Comment comment = new Comment();
        comment.setContent(commentCreateRequestDTO.getContent());
        comment.setStatus(CommentStatus.ACTIVE);
        comment.setType(commentCreateRequestDTO.getCommentType());
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
    public CommentDTO updateCommentContent(SafaUser user, Comment comment, String content) {
        if (!comment.isAuthor(user)) {
            throw new SafaError("Only author of comment is able to edit content.");
        }
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

        if (!comment.isAuthor(user)) {
            throw new SafaError("Only comment author is able to delete comment.");
        }
        commentRepository.delete(comment);
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
}
