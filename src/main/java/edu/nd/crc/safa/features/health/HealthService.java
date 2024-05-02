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
import edu.nd.crc.safa.features.comments.entities.dtos.comments.UndefinedConceptCommentDTO;
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
    private static final String UNKNOWN_CONTENT = "`%s` is used in artifact but undefined in project concepts.";
    private static final String MULTI_CONTENT = "Found multiple, conflicting concepts matching in artifact: %s";
    private static final String PREDICTED_CONTENT = "%s was predicted to be referenced in artifact.";
    private static final String CITED_CONTENT = "`%s` was cited in artifact.";

    private CommentRepository commentRepository;
    private CommentArtifactRepository commentArtifactRepository;
    private CommentConceptRepository commentConceptRepository;
    private ArtifactRepository artifactRepository;
    private ArtifactService artifactService;
    private GenApi genApi;

    /**
     * Performs health checks on artifact and saves them to the database.
     *
     * @param projectVersion Project version being commented on.
     * @param artifactId     ID of artifact being evaluated.
     * @return Response containing health checks.
     */
    public HealthResponse performArtifactHealthChecks(ProjectVersion projectVersion, UUID artifactId) {
        Artifact artifact = artifactService.findById(artifactId);
        List<Artifact> projectArtifacts = artifactRepository.getProjectArtifacts(projectVersion.getProject());
        HealthGenResponse genResponse = generateHealthChecks(projectVersion, artifactId);
        return saveHealthChecks(projectVersion, projectArtifacts, artifact, genResponse);
    }

    /**
     * Calls GEN API to generate health checks.
     *
     * @param projectVersion Project version used to retrieve artifact content.
     * @param artifactId     ID of artifact being evaluated.
     * @return GEN response.
     */
    private HealthGenResponse generateHealthChecks(ProjectVersion projectVersion, UUID artifactId) {
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

    /**
     * Saves health checks as comments under artifact.
     *
     * @param projectVersion   Project version to save comments under.
     * @param projectArtifacts Artifacts in the project.
     * @param artifact         Artifact being evaluated.
     * @param genResponse      GEN API response containing health checks.
     * @return Response object containing comments.
     */
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

    /**
     * Saves undefined entities as concept comments.
     *
     * @param projectVersion    The project version this comment is created in.
     * @param artifact          The artifact being commented on.
     * @param undefinedEntities List of undefined entities in target artifact.
     * @return List of DTOS.
     */
    public List<UndefinedConceptCommentDTO> saveUndefinedEntities(ProjectVersion projectVersion,
                                                                  Artifact artifact,
                                                                  List<String> undefinedEntities) {
        List<Comment> comments = new ArrayList<>();
        Map<Integer, CommentConcept> comment2concept = new HashMap<>();
        for (int i = 0; i < undefinedEntities.size(); i++) {
            String undefinedEntityName = undefinedEntities.get(i);
            String content = String.format(UNKNOWN_CONTENT, undefinedEntityName);
            Comment comment = asMatchedConcept(projectVersion, artifact, CommentType.UNDEFINED_CONCEPT, content);

            CommentConcept commentConcept = new CommentConcept();
            commentConcept.setComment(comment);
            commentConcept.setConceptName(undefinedEntityName);

            comments.add(comment);
            comment2concept.put(i, commentConcept);
        }

        this.commentRepository.saveAll(comments);

        for (Map.Entry<Integer, CommentConcept> entry : comment2concept.entrySet()) {
            Comment comment = comments.get(entry.getKey());
            entry.getValue().setComment(comment);
        }

        this.commentConceptRepository.saveAll(comment2concept.values());

        List<UndefinedConceptCommentDTO> DTOs = new ArrayList<>();
        for (int i = 0; i < comments.size(); i++) {
            CommentConcept commentConcept = comment2concept.get(i);
            DTOs.add(UndefinedConceptCommentDTO.fromComment(commentConcept));
        }
        return DTOs;
    }

    /**
     * Saves predicted links as comment suggestions.
     *
     * @param projectVersion         The project version to create comment in.
     * @param artifact               The artifact being commented on.
     * @param predictedArtifactNames List of predicted artifacts.
     * @param artifactNameLookup     Map of name to artifact.
     * @return List of comments DTOs.
     */
    public List<ArtifactCommentDTO> savePredictedMatches(ProjectVersion projectVersion,
                                                         Artifact artifact,
                                                         List<String> predictedArtifactNames,
                                                         Map<String, Artifact> artifactNameLookup) {

        return saveCommentArtifacts(
            projectVersion,
            artifact,
            predictedArtifactNames,
            n -> Optional.of(artifactNameLookup.get(n)),
            i -> String.format(PREDICTED_CONTENT, predictedArtifactNames.get(i)),
            CommentType.PREDICTED_CONCEPT
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
            i -> String.format(CITED_CONTENT, directMatches.get(i).getId()),
            CommentType.CITED_CONCEPT
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
            loc -> createMultiMatchContent(multiMatches.get(loc)),
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
                                                           Function<Integer, String> contentCreator,
                                                           CommentType commentType) {
        Map<Integer, List<K>> hashMap = new HashMap<>();
        for (int i = 0; i < commentConcepts.size(); i++) {
            hashMap.put(i, commentConcepts.subList(i, i + 1));
        }
        return saveCommentArtifacts(projectVersion, artifact, hashMap, conceptExtractor, contentCreator, commentType);
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
                                                              Function<T, String> contentCreator,
                                                              CommentType commentType) {
        Map<T, Comment> id2comment = new HashMap<>();
        Map<T, List<CommentArtifact>> id2artifacts = new HashMap<>();

        for (Map.Entry<T, List<K>> entry : group2concepts.entrySet()) {
            List<CommentArtifact> entryArtifacts = new ArrayList<>();
            String commentContent = contentCreator.apply(entry.getKey());
            Comment comment = asMatchedConcept(projectVersion, artifact, commentType, commentContent);
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
    private Comment asMatchedConcept(ProjectVersion projectVersion,
                                     Artifact artifact,
                                     CommentType commentType,
                                     String content) {
        Comment comment = new Comment();
        comment.setStatus(CommentStatus.ACTIVE);
        comment.setType(commentType);
        comment.setContent(content);
        comment.setAuthor(null);// generated so no author
        comment.setVersion(projectVersion);
        comment.setArtifact(artifact);
        return comment;
    }

    /**
     * Creates content of multi-concept match comment.
     *
     * @param conceptMatches List of matches.
     * @return Comment content.
     */
    private String createMultiMatchContent(List<ConceptMatchDTO> conceptMatches) {
        String concepts = String.join(",", conceptMatches.stream().map(c -> c.getId()).toList());
        return String.format(MULTI_CONTENT, concepts);
    }
}
