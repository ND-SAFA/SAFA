package edu.nd.crc.safa.features.comments.entities.dtos;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.comments.entities.dtos.comments.ArtifactCommentDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.CommentDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.MultiArtifactCommentDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.UnknownConceptCommentDTO;
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
     * @param commentDTOS              DTOs containing only comment information.
     * @param artifactCommentDTOS      DTOs containing linked concepts.
     * @param multiArtifactCommentDTOS DTOs containing linked artifacts.
     * @param unknownCommentDTOS       Unknown concepts in artifact.
     * @return Response DTO.
     */
    public static ArtifactCommentResponseDTO fromTypes(List<CommentDTO> commentDTOS,
                                                       List<ArtifactCommentDTO> artifactCommentDTOS,
                                                       List<UnknownConceptCommentDTO> unknownCommentDTOS,
                                                       List<MultiArtifactCommentDTO> multiArtifactCommentDTOS) {
        List<CommentDTO> comments = new ArrayList<>();
        List<CommentDTO> flags = new ArrayList<>();
        List<CommentDTO> healthChecks = new ArrayList<>();

        for (CommentDTO commentDTO : commentDTOS) {
            CommentType commentType = commentDTO.getType();

            if (commentType == CommentType.CONVERSATION) {
                comments.add(commentDTO);
            } else if (commentType == CommentType.FLAG) {
                flags.add(commentDTO);
            } else {
                healthChecks.add(commentDTO);
            }
        }

        healthChecks.addAll(unknownCommentDTOS);
        healthChecks.addAll(artifactCommentDTOS);
        healthChecks.addAll(multiArtifactCommentDTOS);

        return new ArtifactCommentResponseDTO(comments, flags, healthChecks);
    }
}
