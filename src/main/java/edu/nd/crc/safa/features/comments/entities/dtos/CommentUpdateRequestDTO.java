package edu.nd.crc.safa.features.comments.entities.dtos;

import lombok.Data;

@Data
public class CommentUpdateRequestDTO {
    /**
     * New content to update comment with.
     */
    private String content;
}
