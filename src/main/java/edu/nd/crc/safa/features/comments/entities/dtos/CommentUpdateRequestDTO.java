package edu.nd.crc.safa.features.comments.entities.dtos;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class CommentUpdateRequestDTO {
    /**
     * New content to update comment with.
     */
    private String content;
}
