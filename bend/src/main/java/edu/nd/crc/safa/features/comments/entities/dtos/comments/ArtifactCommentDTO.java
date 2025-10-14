package edu.nd.crc.safa.features.comments.entities.dtos.comments;

import java.util.UUID;

import edu.nd.crc.safa.features.comments.entities.persistent.CommentArtifact;

import lombok.Data;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode(callSuper = true)
@Data
public class ArtifactCommentDTO extends CommentDTO {
    /**
     * The name of the concept being referenced.
     */
    private UUID conceptArtifactId;

    /**
     * Constructs DTO from CommentConcept.
     *
     * @param commentArtifact The comment concept to copy fields from.
     * @return DTO.
     */
    public static ArtifactCommentDTO fromComment(CommentArtifact commentArtifact) {
        ArtifactCommentDTO dto = new ArtifactCommentDTO();
        CommentDTO.fromComment(commentArtifact.getComment()).copyTo(dto);
        dto.setConceptArtifactId(commentArtifact.getArtifactReferenced().getArtifactId());
        return dto;
    }
}
