package edu.nd.crc.safa.features.comments.entities.dtos.comments;

import edu.nd.crc.safa.features.comments.entities.persistent.CommentConcept;

import lombok.Data;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode(callSuper = true)
@Data
public class ConceptCommentDTO extends CommentDTO {
    /**
     * The name of the concept being referenced.
     */
    private String conceptName;

    /**
     * Constructs DTO from CommentConcept.
     *
     * @param commentConcept The comment concept to copy fields from.
     * @return DTO.
     */
    public static ConceptCommentDTO fromComment(CommentConcept commentConcept) {
        ConceptCommentDTO dto = new ConceptCommentDTO();
        ConceptCommentDTO.fromComment(commentConcept.getComment()).copyTo(dto);
        dto.setConceptName(commentConcept.getConceptName());
        return dto;
    }
}
