package edu.nd.crc.safa.features.comments.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.comments.entities.dtos.ArtifactCommentResponseDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.ArtifactCommentDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.CommentDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.MultiArtifactCommentDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.UndefinedConceptCommentDTO;
import edu.nd.crc.safa.features.comments.entities.persistent.Comment;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentArtifact;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentConcept;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentType;
import edu.nd.crc.safa.features.comments.repositories.CommentArtifactRepository;
import edu.nd.crc.safa.features.comments.repositories.CommentConceptRepository;
import edu.nd.crc.safa.features.comments.repositories.CommentRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class CommentRetrievalService {
    private static final Set<CommentType> TEXT_TYPES = Set.of(CommentType.CONVERSATION, CommentType.FLAG);
    private static final Set<CommentType> SINGLE_ARTIFACT_TYPE = Set.of(CommentType.PREDICTED_CONCEPT,
        CommentType.CITED_CONCEPT);
    private static final Set<CommentType> MULTI_ARTIFACT_TYPES = Set.of(CommentType.CONTRADICTION,
        CommentType.MULTI_MATCHED_CONCEPT);

    private CommentRepository commentRepository;
    private CommentConceptRepository commentConceptRepository;
    private CommentArtifactRepository commentArtifactRepository;
    private ArtifactService artifactService;

    /**
     * Retrieves comments for artifact.
     *
     * @param artifactId ID of artifact whose comments are retrieved.
     * @return Response containing comments grouped by properties.
     */
    public ArtifactCommentResponseDTO getArtifactComments(UUID artifactId) {
        Artifact artifact = artifactService.findById(artifactId);
        List<Comment> textTypes = new ArrayList<>();
        List<Comment> matchedArtifactComments = new ArrayList<>();
        List<Comment> unknownConceptComments = new ArrayList<>();
        List<Comment> multiArtifactComments = new ArrayList<>();

        for (Comment comment : commentRepository.findByArtifactOrderByCreatedAtAsc(artifact)) {
            CommentType commentType = comment.getType();
            if (TEXT_TYPES.contains(commentType)) {
                textTypes.add(comment);
            } else if (SINGLE_ARTIFACT_TYPE.contains(commentType)) {
                matchedArtifactComments.add(comment);
            } else if (commentType.equals(CommentType.UNDEFINED_CONCEPT)) {
                unknownConceptComments.add(comment);
            } else if (MULTI_ARTIFACT_TYPES.contains(commentType)) {
                multiArtifactComments.add(comment);
            } else {
                throw new SafaError(String.format("Unable to place comment type: %s", commentType));
            }
        }

        return ArtifactCommentResponseDTO.fromTypes(
            toTextComments(textTypes),
            toArtifactComments(matchedArtifactComments),
            toUnknownConceptComments(unknownConceptComments),
            toMultiArtifactComments(multiArtifactComments)
        );
    }

    /**
     * Converts comments to base DTOs.
     *
     * @param comments Comments to convert.
     * @return List of DTOs.
     */
    public List<CommentDTO> toTextComments(List<Comment> comments) {
        return comments
            .stream()
            .map(CommentDTO::fromComment)
            .toList();
    }

    /**
     * Hydrates DTO with concept linked to each comment.
     *
     * @param comments List of comments containing linked concepts.
     * @return List of DTOs.
     */
    public List<ArtifactCommentDTO> toArtifactComments(List<Comment> comments) {
        List<UUID> commentIds = comments.stream().map(Comment::getId).toList();
        List<ArtifactCommentDTO> dtos = new ArrayList<>();
        for (CommentArtifact commentArtifact : commentArtifactRepository.findAllByComment_IdIn(commentIds)) {
            dtos.add(ArtifactCommentDTO.fromComment(commentArtifact));
        }
        return dtos;
    }

    /**
     * Retrieves concept associated with each comment and construct unknown concept comment.
     *
     * @param comments Comments with associated concepts.
     * @return List of DTOS.
     */
    public List<UndefinedConceptCommentDTO> toUnknownConceptComments(List<Comment> comments) {
        List<UUID> commentIds = comments.stream().map(Comment::getId).toList();
        List<CommentConcept> commentConcepts = commentConceptRepository.findAllByComment_IdIn(commentIds);
        return commentConcepts.stream().map(UndefinedConceptCommentDTO::fromComment).toList();
    }

    /**
     * Hydrates comments with each comments multiple linked artifacts.
     *
     * @param comments Comments to convert to MultiArtifactDTOs.
     * @return DTOs.
     */
    public List<MultiArtifactCommentDTO> toMultiArtifactComments(List<Comment> comments) {
        List<UUID> commentIds = comments.stream().map(Comment::getId).toList();
        Map<Comment, List<CommentArtifact>> commentId2artifacts = ProjectDataStructures.createGroupLookup(
            commentArtifactRepository.findAllByComment_IdIn(commentIds),
            CommentArtifact::getComment
        );
        return commentId2artifacts.entrySet().stream().map(e -> {
            List<UUID> artifactIds = e.getValue()
                .stream()
                .map(c -> c.getArtifactReferenced().getArtifactId())
                .toList();
            return MultiArtifactCommentDTO.fromComment(e.getKey(), artifactIds);
        }).toList();
    }
}
