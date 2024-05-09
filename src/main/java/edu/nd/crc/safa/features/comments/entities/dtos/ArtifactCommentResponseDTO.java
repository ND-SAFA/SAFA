package edu.nd.crc.safa.features.comments.entities.dtos;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.comments.entities.dtos.comments.CommentDTO;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentType;

import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
public class ArtifactCommentResponseDTO {
    /**
     * User comments on artifact.
     */
    private List<CommentDTO> comments;
    /**
     * User flags on artifacts.
     */
    private List<CommentDTO> flags;
    /**
     * Generated warnings on artifacts.
     */
    private List<CommentDTO> healthChecks;

    /**
     * Creates response DTO from the different types of comments, placing each into its corresponding DTO property.
     *
     * @param id2dto Map of comment ID to DTO.
     * @return Response DTO.
     */
    public static ArtifactCommentResponseDTO fromTypes(Map<UUID, CommentDTO> id2dto) {
        List<CommentDTO> comments = new ArrayList<>();
        List<CommentDTO> flags = new ArrayList<>();
        List<CommentDTO> healthChecks = new ArrayList<>();

        for (Map.Entry<UUID, CommentDTO> entry : id2dto.entrySet()) {
            CommentDTO dto = entry.getValue();
            CommentType commentType = dto.getType();

            if (commentType == CommentType.CONVERSATION) {
                comments.add(dto);
            } else if (commentType == CommentType.FLAG) {
                flags.add(dto);
            } else {
                healthChecks.add(dto);
            }
        }

        return new ArtifactCommentResponseDTO(comments, flags, healthChecks);
    }
}
