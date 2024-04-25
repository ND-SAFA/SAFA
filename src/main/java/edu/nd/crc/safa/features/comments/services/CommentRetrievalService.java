package edu.nd.crc.safa.features.comments.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.comments.entities.dtos.ArtifactCommentResponseDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.CommentDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.ConceptCommentDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.MultiArtifactCommentDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.MultiConceptCommentDTO;
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
    private static final Set<CommentType> TEXT_TYPES = Set.of(CommentType.CONVERSATION, CommentType.FLAG, CommentType.SUGGESTION);
    private static final Set<CommentType> CONCEPT_TYPES = Set.of(CommentType.MATCHED_CONCEPT, CommentType.UNKNOWN_CONCEPT);
    private static final Set<CommentType> ARTIFACT_TYPES = Set.of(CommentType.CONTRADICTION);
    private static final Set<CommentType> MULTI_CONCEPT_TYPES = Set.of(CommentType.MULTI_MATCHED_CONCEPT);

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
        List<Comment> conceptComments = new ArrayList<>();
        List<Comment> artifactComments = new ArrayList<>();
        List<Comment> multiConceptComments = new ArrayList<>();

        for (Comment comment : commentRepository.findByArtifactOrderByCreatedAsc(artifact)) {
            CommentType commentType = comment.getType();
            if (TEXT_TYPES.contains(commentType)) {
                textTypes.add(comment);
            } else if (CONCEPT_TYPES.contains(commentType)) {
                conceptComments.add(comment);
            } else if (ARTIFACT_TYPES.contains(commentType)) {
                artifactComments.add(comment);
            } else if (MULTI_CONCEPT_TYPES.contains(commentType)) {
                multiConceptComments.add(comment);
            } else {
                throw new SafaError(String.format("Unable to place comment type: %s", commentType));
            }
        }

        return ArtifactCommentResponseDTO.fromTypes(
            toCommentDTOS(textTypes),
            toConceptCommentDTOS(conceptComments),
            toArtifactCommentDTOS(artifactComments),
            toMultiConceptCommentDTOS(multiConceptComments)
        );
    }

    /**
     * Converts comments to base DTOs.
     *
     * @param comments Comments to convert.
     * @return List of DTOs.
     */
    public List<CommentDTO> toCommentDTOS(List<Comment> comments) {
        return comments
            .stream()
            .map(CommentDTO::fromComment)
            .toList();
    }

    /**
     * Hydrates comments with each comments multiple linked artifacts.
     *
     * @param comments Comments to convert to MultiArtifactDTOs.
     * @return DTOs.
     */
    public List<MultiArtifactCommentDTO> toArtifactCommentDTOS(List<Comment> comments) {
        List<UUID> commentIds = comments.stream().map(Comment::getId).toList();
        List<MultiArtifactCommentDTO> dtos = new ArrayList<>();
        Map<UUID, List<CommentArtifact>> commentId2artifacts = ProjectDataStructures.createGroupLookup(
            commentArtifactRepository.findAllById(commentIds),
            c -> c.getComment().getId()
        );
        return comments
            .stream()
            .map(comment -> {
                List<CommentArtifact> commentArtifacts = commentId2artifacts.get(comment.getId());
                List<UUID> artifactIds = commentArtifacts.stream().map(c -> c.getArtifact().getArtifactId()).toList();
                return MultiArtifactCommentDTO.fromComment(comment, artifactIds);
            }).toList();
    }

    /**
     * Hydrates comments with each comments multiple linked concepts.
     *
     * @param comments The comments to convert to DTOs.
     * @return List of DTOs.
     */
    public List<MultiConceptCommentDTO> toMultiConceptCommentDTOS(List<Comment> comments) {
        List<MultiConceptCommentDTO> dtos = new ArrayList<>();
        List<UUID> commentIds = comments.stream().map(Comment::getId).toList();
        Map<UUID, List<CommentConcept>> comment2concepts = ProjectDataStructures.createGroupLookup(
            commentConceptRepository.findAllById(commentIds),
            c -> c.getComment().getId()
        );
        return comments
            .stream()
            .map(comment -> {
                List<CommentConcept> commentConcepts = comment2concepts.get(comment.getId());
                List<String> concepts = commentConcepts.stream().map(CommentConcept::getConceptName).toList();
                return MultiConceptCommentDTO.fromComment(comment, concepts);
            }).toList();
    }

    /**
     * Hydrates DTO with concept linked to each comment.
     *
     * @param comments List of comments containing linked concepts.
     * @return List of DTOs.
     */
    public List<ConceptCommentDTO> toConceptCommentDTOS(List<Comment> comments) {
        List<UUID> commentIds = comments.stream().map(Comment::getId).toList();
        List<ConceptCommentDTO> dtos = new ArrayList<>();
        for (CommentConcept commentConcept : commentConceptRepository.findAllById(commentIds)) {
            dtos.add(ConceptCommentDTO.fromComment(commentConcept));
        }
        return dtos;
    }
}
