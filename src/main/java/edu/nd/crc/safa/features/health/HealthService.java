package edu.nd.crc.safa.features.health;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.function.Function;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.ArtifactCommentDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.MultiArtifactCommentDTO;
import edu.nd.crc.safa.features.comments.entities.dtos.comments.UnknownConceptCommentDTO;
import edu.nd.crc.safa.features.comments.entities.persistent.Comment;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentArtifact;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentConcept;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentStatus;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentType;
import edu.nd.crc.safa.features.comments.repositories.CommentArtifactRepository;
import edu.nd.crc.safa.features.comments.repositories.CommentConceptRepository;
import edu.nd.crc.safa.features.comments.repositories.CommentRepository;
import edu.nd.crc.safa.features.generation.api.GenApi;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

import lombok.AllArgsConstructor;
import org.jetbrains.annotations.NotNull;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class HealthService {
    private CommentRepository commentRepository;
    private CommentArtifactRepository commentArtifactRepository;
    private CommentConceptRepository commentConceptRepository;
    private ArtifactRepository artifactRepository;
    private ArtifactService artifactService;
    private GenApi genApi;

    public HealthResponse generateHealthChecks(ProjectVersion projectVersion, UUID id) {
        Artifact artifact = artifactService.findById(id);
        List<Artifact> projectArtifacts = artifactRepository.getProjectArtifacts(projectVersion.getProject());
        HealthGenResponse genResponse = genHealthChecks(projectVersion, id);
        return saveHealthChecks(projectVersion, projectArtifacts, artifact, genResponse);
    }

    private HealthGenResponse genHealthChecks(ProjectVersion projectVersion, UUID artifactId) {
        List<ArtifactAppEntity> artifacts = artifactService.getAppEntities(projectVersion);
        List<ArtifactAppEntity> projectArtifacts =
            artifacts.stream().filter(a -> !a.getId().equals(artifactId)).toList();
        List<ArtifactAppEntity> targetArtifactQuery =
            artifacts.stream().filter(a -> !a.getId().equals(artifactId)).toList();

        if (targetArtifactQuery.isEmpty()) {
            throw new SafaError("Unable to find artifact with given ID.");
        }

        return genApi.generateHealthChecks(
            projectArtifacts.stream().map(GenerationArtifact::new).toList(),
            new GenerationArtifact(targetArtifactQuery.get(0))
        );
    }

    @NotNull
    private HealthResponse saveHealthChecks(ProjectVersion projectVersion,
                                            List<Artifact> projectArtifacts,
                                            Artifact artifact,
                                            HealthGenResponse genResponse) {
        HealthResponse response = new HealthResponse();
        Map<String, Artifact> artifactNameLookup = ProjectDataStructures.createEntityLookup(
            projectArtifacts,
            Artifact::getName
        );
        // save direct matches as links
        List<ArtifactCommentDTO> directMatches = saveDirectMatches(
            projectVersion,
            artifact,
            artifactNameLookup,
            genResponse.getMatches());
        response.addHealthChecks(directMatches);
        // save multi-matches as warning
        response.addHealthChecks(saveMultiMatchedConcepts(projectVersion, artifact, genResponse.getMultiMatches(),
            artifactNameLookup));
        // save predicted matches as
        response.addHealthChecks(savePredictedMatches(projectVersion, artifact, genResponse.getPredictedMatches(),
            artifactNameLookup));
        // save undefined entities
        response.addHealthChecks(saveUndefinedEntities(projectVersion, artifact, genResponse.getUndefinedEntities()));
        return response;
    }

    public List<UnknownConceptCommentDTO> saveUndefinedEntities(ProjectVersion projectVersion,
                                                                Artifact artifact,
                                                                List<String> undefinedEntities) {
        List<Comment> comments = new ArrayList<>();
        Map<Comment, CommentConcept> comment2concept = new HashMap<>();
        for (String undefinedEntityName : undefinedEntities) {
            Comment comment = asMatchedConcept(projectVersion, artifact, CommentType.UNKNOWN_CONCEPT);

            CommentConcept commentConcept = new CommentConcept();
            commentConcept.setComment(comment);
            commentConcept.setConceptName(undefinedEntityName);

            comments.add(comment);
            comment2concept.put(comment, commentConcept);
        }

        this.commentRepository.saveAll(comments);

        for (Map.Entry<Comment, CommentConcept> entry : comment2concept.entrySet()) {
            entry.getValue().setComment(entry.getKey());
        }

        this.commentConceptRepository.saveAll(comment2concept.values());

        List<UnknownConceptCommentDTO> DTOs = new ArrayList<>();
        for (Comment comment : comments) {
            CommentConcept commentConcept = comment2concept.get(comment);
            DTOs.add(UnknownConceptCommentDTO.fromComment(commentConcept));
        }
        return DTOs;
    }

    /**
     * Saves predicted links as comment suggestions.
     *
     * @param projectVersion     The project version to create comment in.
     * @param artifact           The artifact being commented on.
     * @param predictedArtifacts List of predicted artifacts.
     * @param artifactNameLookup Map of name to artifact.
     * @return List of comments DTOs.
     */
    public List<ArtifactCommentDTO> savePredictedMatches(ProjectVersion projectVersion,
                                                         Artifact artifact,
                                                         List<GenerationArtifact> predictedArtifacts,
                                                         Map<String, Artifact> artifactNameLookup) {

        return saveCommentArtifacts(
            projectVersion,
            artifact,
            predictedArtifacts,
            g -> Optional.of(artifactNameLookup.get(g.getId())),
            CommentType.MATCHED_CONCEPT
        )
            .stream()
            .map(ArtifactCommentDTO::fromComment)
            .toList();
    }

    /**
     * Creates concept comments for each direct match found.
     *
     * @param projectVersion     The project version this comment was created in.
     * @param artifact           The artifact that this comment was created for.
     * @param artifactNameLookup Map of name to artifact.
     * @param directMatches      The direct matches to create comments for.
     * @return List of concepts comments generated for artifact.
     */
    public List<ArtifactCommentDTO> saveDirectMatches(ProjectVersion projectVersion,
                                                      Artifact artifact,
                                                      Map<String, Artifact> artifactNameLookup,
                                                      List<ConceptMatchDTO> directMatches) {
        return saveCommentArtifacts(
            projectVersion,
            artifact,
            directMatches,
            c -> Optional.of(artifactNameLookup.get(c.getId())),
            CommentType.MATCHED_CONCEPT
        ).stream().map(ArtifactCommentDTO::fromComment).toList();
    }

    /**
     * Saves each group of matched concepts to the database and creates their representation.
     *
     * @param projectVersion     Project version the comment is created in.
     * @param artifact           The artifact being commented on.
     * @param multiMatches       Map containing groups of concept matches.
     * @param artifactNameLookup Map of artifact name to artifact entity.
     * @return List of DTOs.
     */
    public List<MultiArtifactCommentDTO> saveMultiMatchedConcepts(ProjectVersion projectVersion,
                                                                  Artifact artifact,
                                                                  Map<Integer, List<ConceptMatchDTO>> multiMatches,
                                                                  Map<String, Artifact> artifactNameLookup) {
        List<CommentArtifact> commentArtifacts = saveCommentArtifacts(
            projectVersion,
            artifact,
            multiMatches,
            c -> Optional.of(artifactNameLookup.get(c.getId())),
            CommentType.MULTI_MATCHED_CONCEPT);

        Map<Comment, List<CommentArtifact>> commentConceptLookup =
            ProjectDataStructures.createGroupLookup(commentArtifacts, CommentArtifact::getComment);

        return commentConceptLookup
            .entrySet()
            .stream()
            .map(entry -> {
                List<UUID> artifactIds =
                    entry.getValue().stream()
                        .map(c -> c.getArtifactReferenced().getName())
                        .map(name -> artifactNameLookup.get(name).getArtifactId())
                        .toList();
                return MultiArtifactCommentDTO.fromComment(entry.getKey(), artifactIds);
            }).toList();
    }

    /**
     * Creates list of comment concepts.
     *
     * @param projectVersion  The project version the comment is created in.
     * @param artifact        The artifact being commented on.
     * @param commentConcepts List of concepts referenced in coment.
     * @return List of concept comments created.
     */
    private <K> List<CommentArtifact> saveCommentArtifacts(ProjectVersion projectVersion,
                                                           Artifact artifact,
                                                           List<K> commentConcepts,
                                                           Function<K, Optional<Artifact>> conceptExtractor,
                                                           CommentType commentType) {
        Map<String, List<K>> hashMap = new HashMap<>();
        hashMap.put("ID", commentConcepts);
        return saveCommentArtifacts(projectVersion, artifact, hashMap, conceptExtractor, commentType);
    }

    /**
     * Saves comments and associated concepts.
     *
     * @param projectVersion The project version the comment is created in.
     * @param artifact       The artifact being commented on.
     * @param group2concepts Map of group ID to list of concepts in that group. Comment is created for each group.
     * @param <T>            Type of ID used in map.
     * @param commentType    Type of comment being made.
     * @return List of CommentConcepts saved to database.
     */
    private <T, K> List<CommentArtifact> saveCommentArtifacts(ProjectVersion projectVersion,
                                                              Artifact artifact,
                                                              Map<T, List<K>> group2concepts,
                                                              Function<K, Optional<Artifact>> artifactLookup,
                                                              CommentType commentType) {
        Map<T, Comment> id2comment = new HashMap<>();
        Map<T, List<CommentArtifact>> id2artifacts = new HashMap<>();

        for (Map.Entry<T, List<K>> entry : group2concepts.entrySet()) {
            List<CommentArtifact> entryArtifacts = new ArrayList<>();
            Comment comment = asMatchedConcept(projectVersion, artifact, commentType);
            for (K dto : entry.getValue()) {
                Optional<Artifact> artifactOptional = artifactLookup.apply(dto);
                if (artifactOptional.isEmpty()) {
                    continue;
                }

                Artifact artifactReferenced = artifactOptional.get();

                CommentArtifact commentArtifact = new CommentArtifact();
                commentArtifact.setArtifactReferenced(artifactReferenced);
                commentArtifact.setComment(comment);
                entryArtifacts.add(commentArtifact);
            }
            id2comment.put(entry.getKey(), comment);
            id2artifacts.put(entry.getKey(), entryArtifacts);
        }

        this.commentRepository.saveAll(id2comment.values());

        for (Map.Entry<T, Comment> entry : id2comment.entrySet()) {
            List<CommentArtifact> entryArtifacts = id2artifacts.get(entry.getKey());
            for (CommentArtifact entryArtifact : entryArtifacts) {
                entryArtifact.setComment(entry.getValue());
            }
        }

        this.commentArtifactRepository.saveAll(id2artifacts.values().stream().flatMap(List::stream).toList());

        List<CommentArtifact> commentArtifactDTOS = new ArrayList<>();
        for (Map.Entry<T, Comment> entry : id2comment.entrySet()) {
            List<CommentArtifact> entryArtifacts = id2artifacts.get(entry.getKey());
            Comment comment = entry.getValue();
            for (CommentArtifact entityConcept : entryArtifacts) {
                entityConcept.setComment(comment);
                commentArtifactDTOS.add(entityConcept);
            }
        }
        return commentArtifactDTOS;
    }

    /**
     * Creates comment of type MatchedConcept on given artifact.
     *
     * @param projectVersion Project version that comment is created in.
     * @param artifact       The artifact being commented on.
     * @return Base comment of type MatchedConcept.
     */
    private Comment asMatchedConcept(ProjectVersion projectVersion, Artifact artifact, CommentType commentType) {
        Comment comment = new Comment();
        comment.setStatus(CommentStatus.ACTIVE);
        comment.setType(commentType);
        comment.setAuthor(null);// generated so no author
        comment.setVersion(projectVersion);
        comment.setArtifact(artifact);
        return comment;
    }
}
