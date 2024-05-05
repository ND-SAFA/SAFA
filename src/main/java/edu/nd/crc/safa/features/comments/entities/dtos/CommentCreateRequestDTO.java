package edu.nd.crc.safa.features.comments.entities.dtos;

import java.util.UUID;

import edu.nd.crc.safa.features.comments.entities.persistent.CommentType;

import lombok.Data;
import org.jetbrains.annotations.NotNull;

@Data
public class CommentCreateRequestDTO {
    /**
     * Text in comment.
     */
    @NotNull
    private String content;
    /**
     * Type of comment to create.
     */
    @NotNull
    private CommentType type;
    /**
     * ID of version that comment was created in.
     */
    @NotNull
    private UUID versionId;
}
