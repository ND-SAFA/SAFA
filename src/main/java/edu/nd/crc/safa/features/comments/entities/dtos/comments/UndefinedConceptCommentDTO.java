package edu.nd.crc.safa.features.comments.entities.dtos.comments;

import edu.nd.crc.safa.features.comments.entities.persistent.CommentConcept;

import lombok.Data;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode(callSuper = true)
@Data
public class UndefinedConceptCommentDTO extends CommentDTO {
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
    public static UndefinedConceptCommentDTO fromComment(CommentConcept commentConcept) {
        UndefinedConceptCommentDTO dto = new UndefinedConceptCommentDTO();
        CommentDTO.fromComment(commentConcept.getComment()).copyTo(dto);
        dto.setUndefinedConcept(commentConcept.getConceptName());
        return dto;
    }
}
