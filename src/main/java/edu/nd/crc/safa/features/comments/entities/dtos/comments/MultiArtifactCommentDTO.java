package edu.nd.crc.safa.features.comments.entities.dtos.comments;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.comments.entities.persistent.Comment;

import lombok.Data;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode(callSuper = true)
@Data
public class MultiArtifactCommentDTO extends CommentDTO {
    /**
     * List of ids linked to artifact.
     */
    private List<UUID> artifactIds;

    /**
     * Creates DTO from comment and associated artifacts.
     *
     * @param comment     The base comment.
     * @param artifactIds Linked artifact ids.
     * @return DTO.
     */
    public static MultiArtifactCommentDTO fromComment(Comment comment, List<UUID> artifactIds) {
        MultiArtifactCommentDTO dto = new MultiArtifactCommentDTO();
        ArtifactCommentDTO.fromComment(comment).copyTo(dto);
        dto.setArtifactIds(artifactIds);
        return dto;
    }
}
