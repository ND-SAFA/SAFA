package edu.nd.crc.safa.features.comments.entities.dtos.comments;

import java.time.LocalDateTime;
import java.util.UUID;

import edu.nd.crc.safa.features.comments.entities.persistent.Comment;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentStatus;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentType;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Data;

@Data
public class CommentDTO {
    /**
     * ID of comment
     */
    private UUID id;
    /**
     * Text of comment
     */
    private String content;
    /**
     * ID of user who created comment.
     */
    private String userId;
    /**
     * ID of version this comment was created in.
     */
    private UUID versionId;
    /**
     * Status of comment.
     */
    private CommentStatus status;
    /**
     * Type of comment.
     */
    private CommentType type;
    /**
     * Timestamp of when this comment was created.
     */
    private LocalDateTime createdAt;
    /**
     * Timestamp of when this comment was last updated.
     */
    private LocalDateTime updatedAt;

    /**
     * Creates DTO from persistent entity.
     *
     * @param comment Persistent comment entity.
     * @return DTO entity.
     */
    public static CommentDTO fromComment(Comment comment) {
        CommentDTO dto = new CommentDTO();
        dto.setId(comment.getId());
        dto.setContent(comment.getContent());
        dto.setType(comment.getType());
        dto.setStatus(comment.getStatus());
        dto.setVersionId(comment.getVersion().getVersionId());
        dto.setCreatedAt(comment.getCreatedAt());
        dto.setUpdatedAt(comment.getUpdatedAt());

        SafaUser author = comment.getAuthor();
        if (author != null) {
            dto.setUserId(author.getEmail());
        }
        return dto;
    }

    /**
     * Copies fields from instance to other.
     *
     * @param other DTO to copy fields to.
     */
    public void copyTo(CommentDTO other) {
        other.setId(this.id);
        other.setContent(this.content);
        other.setUserId(this.userId);
        other.setVersionId(this.versionId);
        other.setStatus(this.status);
        other.setType(this.type);
        other.setCreatedAt(this.createdAt);
        other.setUpdatedAt(this.updatedAt);
    }
}
