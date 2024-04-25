package edu.nd.crc.safa.features.comments.entities.dtos.comments;

import java.util.List;

import edu.nd.crc.safa.features.comments.entities.persistent.Comment;

import lombok.Data;

@Data
public class MultiConceptCommentDTO extends CommentDTO {
    /**
     * List of matched concepts.
     */
    private List<String> concepts;

    /**
     * Creates DTO from base comment and linked concepts.
     *
     * @param comment  The base comment.
     * @param concepts Linked concepts.
     * @return DTO.
     */
    public static MultiConceptCommentDTO fromComment(Comment comment, List<String> concepts) {
        MultiConceptCommentDTO dto = new MultiConceptCommentDTO();
        ConceptCommentDTO.fromComment(comment).copyTo(dto);
        dto.setConcepts(concepts);
        return dto;
    }
}
