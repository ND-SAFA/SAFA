package edu.nd.crc.safa.features.comments.entities.dtos.comments;

import edu.nd.crc.safa.features.comments.entities.persistent.CommentConcept;

import lombok.Data;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode(callSuper = true)
@Data
public class UnknownConceptCommentDTO extends CommentDTO {
    /**
     * The concept found in artifact but undefined in project.
     */
    private String undefinedConcept;

    /**
     * Constructs DTO from CommentConcept.
     *
     * @param commentConcept The comment concept to copy fields from.
     * @return DTO.
     */
    public static UnknownConceptCommentDTO fromComment(CommentConcept commentConcept) {
        UnknownConceptCommentDTO dto = new UnknownConceptCommentDTO();
        CommentDTO.fromComment(commentConcept.getComment()).copyTo(dto);
        dto.setUndefinedConcept(commentConcept.getConceptName());
        return dto;
    }
}
