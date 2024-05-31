package edu.nd.crc.safa.features.health;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.function.Function;
import java.util.stream.Collectors;

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
import edu.nd.crc.safa.features.generation.common.GenerationLink;
import edu.nd.crc.safa.features.health.entities.ConceptMatchDTO;
import edu.nd.crc.safa.features.health.entities.HealthResponseDTO;
import edu.nd.crc.safa.features.health.entities.gen.GenConceptResponse;
import edu.nd.crc.safa.features.health.entities.gen.GenHealthResponse;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

import lombok.AllArgsConstructor;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class HealthService {
    private static final String UNKNOWN_CONTENT = "`%s` is used in artifact but undefined in project concepts.";
    private static final String MULTI_CONTENT = "Found multiple, conflicting concepts matching in artifact: %s";
    private static final String PREDICTED_CONTENT = "The entity `%s` was predicted to matched with concept `%s`.";
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
     * @param artifact       Artifact generating health checks for.
     * @return Response containing health checks.
     */
    public HealthResponseDTO performArtifactHealthChecks(ProjectVersion projectVersion, ArtifactAppEntity artifact) {
        List<Artifact> projectArtifacts = artifactRepository.getProjectArtifacts(projectVersion.getProject().getId());
        GenHealthResponse genResponse = generateHealthChecks(projectVersion, artifact);
        Artifact targetArtifact = null;
        if (artifact.getId() != null) {
            targetArtifact = artifactService.findById(artifact.getId());
        }
        return saveHealthChecks(projectVersion, projectArtifacts, targetArtifact, genResponse);
    }

    /**
     * Deletes health checks associated with artifact.
     *
     * @param artifact The artifact to delete health checks for.
     */
    public void clearArtifactHealthChecks(Artifact artifact) {
        List<Comment> artifactHealthChecks = this.commentRepository.findByArtifactOrderByCreatedAtAsc(artifact)
            .stream()
            .filter(c -> c.getType().isHealthCheck())
            .toList();
        this.commentRepository.deleteAll(artifactHealthChecks);
    }

    /**
     * Calls GEN API to generate health checks.
     *
     * @param projectVersion Project version used to retrieve artifact content.
     * @param targetArtifact Target artifact being checks.
     * @return GEN response.
     */
    private GenHealthResponse generateHealthChecks(ProjectVersion projectVersion, ArtifactAppEntity targetArtifact) {
        List<GenerationArtifact> artifacts = artifactService
            .getAppEntities(projectVersion).stream().map(GenerationArtifact::new).collect(Collectors.toList());
        GenerationArtifact targetGenArtifact = new GenerationArtifact(targetArtifact);
        if (targetArtifact.getId() == null) {
            artifacts.add(targetGenArtifact);
        }
        return genApi.generateHealthChecks(artifacts, targetGenArtifact);
    }

    /**
     * Saves health checks as comments under artifact.
     *
     * @param projectVersion   Project version to save comments under.
     * @param projectArtifacts Artifacts in the project.
     * @param targetArtifact   Artifact being evaluated.
     * @param genResponse      GEN API response containing health checks.
     * @return Response object containing comments.
     */
    @NotNull
    private HealthResponseDTO saveHealthChecks(ProjectVersion projectVersion,
                                               List<Artifact> projectArtifacts,
                                               @Nullable Artifact targetArtifact,
                                               GenHealthResponse genResponse) {
        GenConceptResponse genConceptResponse = genResponse.getConceptMatches();
        HealthResponseDTO response = new HealthResponseDTO();
        Map<String, Artifact> artifactNameLookup = ProjectDataStructures.createEntityLookup(
            projectArtifacts,
            Artifact::getName
        );
        // save direct matches as links
        response.addHealthChecks(
            saveDirectMatches(
                projectVersion,
                targetArtifact,
                artifactNameLookup,
                genConceptResponse.getMatches()
            )
        );
        // save multi-matches as warning
        response.addHealthChecks(
            saveMultiMatchedConcepts(
                projectVersion, targetArtifact, genConceptResponse.getMultiMatches(), artifactNameLookup
            )
        );
        // save predicted matches as
        response.addHealthChecks(
            savePredictedMatches(
                projectVersion, targetArtifact, genConceptResponse.getPredictedMatches(), artifactNameLookup
            )
        );
        // save undefined entities
        response.addHealthChecks(
            saveUndefinedEntities(
                projectVersion, targetArtifact, genConceptResponse.getUndefinedEntities()
            )
        );

        response.addHealthChecks(saveContradictions(projectVersion, targetArtifact, artifactNameLookup, genResponse));
        return response;
    }

    /**
     * Saves contradictions found in gen response.
     *
     * @param projectVersion     Project version used to save comment under.
     * @param artifact           The artifact being commented on.
     * @param artifactNameLookup Artifact Lookup table indexed by name.
     * @param response           Gen Response.
     * @return List of multi-artifact DTOs.
     */
    public List<MultiArtifactCommentDTO> saveContradictions(ProjectVersion projectVersion,
                                                            Artifact artifact,
                                                            Map<String, Artifact> artifactNameLookup,
                                                            GenHealthResponse response) {
        List<String> conflictingIds = response.getContradictions().getConflictingIds();
        if (conflictingIds == null || conflictingIds.isEmpty()) {
            return new ArrayList<>();
        }
        Map<Integer, List<CommentArtifact>> commentArtifactMap = createCommentArtifactMap(
            projectVersion,
            artifact,
            listToMap(conflictingIds, false),
            i -> response.getContradictions().getExplanation(),
            c -> Optional.of(artifactNameLookup.get(c)),
            CommentType.CONTRADICTION
        );

        return getMultiArtifactCommentDTOS(artifact != null, commentArtifactMap);
    }

    /**
     * Creates concept comments for each direct match found.
     *
     * @param projectVersion     The project version this comment was created in.
     * @param targetArtifact     The artifact that this comment was created for.
     * @param artifactNameLookup Map of name to artifact.
     * @param directMatches      The direct matches to create comments for.
     * @return List of concepts comments generated for artifact.
     */
    public List<ArtifactCommentDTO> saveDirectMatches(ProjectVersion projectVersion,
                                                      Artifact targetArtifact,
                                                      Map<String, Artifact> artifactNameLookup,
                                                      List<ConceptMatchDTO> directMatches) {

        Map<Integer, List<CommentArtifact>> commentArtifactMap = createCommentArtifactMap(
            projectVersion,
            targetArtifact,
            listToMap(directMatches, true),
            i -> String.format(CITED_CONTENT, directMatches.get(i).getId()),
            c -> Optional.of(artifactNameLookup.get(c.getId())),
            CommentType.CITED_CONCEPT
        );

        if (targetArtifact != null) {
            saveCommentArtifactMap(commentArtifactMap);
        }

        return mapToDTOs(commentArtifactMap,
            commentArtifacts -> ArtifactCommentDTO.fromComment(commentArtifacts.get(0)));
    }

    /**
     * Saves predicted links as comment suggestions.
     *
     * @param projectVersion         The project version to create comment in.
     * @param targetArtifact         The artifact being commented on.
     * @param predictedArtifactNames List of predicted artifacts.
     * @param artifactNameLookup     Map of name to artifact.
     * @return List of comments DTOs.
     */
    public List<ArtifactCommentDTO> savePredictedMatches(ProjectVersion projectVersion,
                                                         Artifact targetArtifact,
                                                         List<GenerationLink> predictedArtifactNames,
                                                         Map<String, Artifact> artifactNameLookup) {

        Map<Integer, List<CommentArtifact>> commentArtifactMap = createCommentArtifactMap(
            projectVersion,
            targetArtifact,
            listToMap(predictedArtifactNames, true),
            i -> generatePredictionContent(predictedArtifactNames.get(i)),
            n -> Optional.of(artifactNameLookup.get(n.getTarget())), // source=entity, target=concept
            CommentType.PREDICTED_CONCEPT
        );

        if (targetArtifact != null) {
            saveCommentArtifactMap(commentArtifactMap);
        }

        return mapToDTOs(commentArtifactMap,
            commentArtifacts -> ArtifactCommentDTO.fromComment(commentArtifacts.get(0)));
    }

    /**
     * Generates the content of the predicted link.
     *
     * @param link Contains entity in target artifact as source and the concept as target.
     * @return Content.
     */
    private String generatePredictionContent(GenerationLink link) {
        String entityName = link.getSource();
        String conceptName = link.getTarget();
        return String.format(PREDICTED_CONTENT, entityName, conceptName);
    }

    /**
     * Saves each group of matched concepts to the database and creates their representation.
     *
     * @param projectVersion     Project version the comment is created in.
     * @param targetArtifact     The artifact being commented on.
     * @param multiMatches       Map containing groups of concept matches.
     * @param artifactNameLookup Map of artifact name to artifact entity.
     * @return List of DTOs.
     */
    public List<MultiArtifactCommentDTO> saveMultiMatchedConcepts(ProjectVersion projectVersion,
                                                                  Artifact targetArtifact,
                                                                  Map<Integer, List<ConceptMatchDTO>> multiMatches,
                                                                  Map<String, Artifact> artifactNameLookup) {

        Map<Integer, List<CommentArtifact>> commentArtifactMap = createCommentArtifactMap(
            projectVersion,
            targetArtifact,
            multiMatches,
            loc -> createMultiMatchContent(multiMatches.get(loc)),
            c -> Optional.of(artifactNameLookup.get(c.getId())),
            CommentType.MULTI_MATCHED_CONCEPT
        );

        return getMultiArtifactCommentDTOS(targetArtifact != null, commentArtifactMap);
    }

    /**
     * Saves undefined entities as concept comments.
     *
     * @param projectVersion    The project version this comment is created in.
     * @param targetArtifact    The artifact being commented on.
     * @param undefinedEntities List of undefined entities in target artifact.
     * @return List of DTOS.
     */
    public List<UndefinedConceptCommentDTO> saveUndefinedEntities(ProjectVersion projectVersion,
                                                                  Artifact targetArtifact,
                                                                  List<GenerationArtifact> undefinedEntities) {
        List<CommentConcept> commentConcepts = createConceptComments(projectVersion, targetArtifact, undefinedEntities);

        List<Comment> comments = commentConcepts.stream().map(CommentConcept::getComment).toList();
        if (targetArtifact != null) {
            this.commentRepository.saveAll(comments);
            this.commentConceptRepository.saveAll(commentConcepts);
        }

        return commentConcepts.stream().map(UndefinedConceptCommentDTO::fromComment).toList();
    }

    private <T> void saveCommentArtifactMap(Map<T, List<CommentArtifact>> commentArtifactMap) {
        List<Comment> comments =
            commentArtifactMap.values().stream().map(commentArtifacts -> commentArtifacts.get(0).getComment()).toList();
        this.commentRepository.saveAll(comments);
        List<CommentArtifact> commentArtifacts = commentArtifactMap.values().stream().flatMap(List::stream).toList();
        this.commentArtifactRepository.saveAll(commentArtifacts);
    }

    private <K, T> List<T> mapToDTOs(Map<K, List<CommentArtifact>> commentArtifactMap,
                                     Function<List<CommentArtifact>, T> dtoCreator) {
        return commentArtifactMap.values().stream().map(dtoCreator).toList();
    }

    private List<CommentConcept> createConceptComments(ProjectVersion projectVersion,
                                                       Artifact targetArtifact,
                                                       List<GenerationArtifact> undefinedEntities) {
        List<CommentConcept> conceptComments = new ArrayList<>();
        for (GenerationArtifact undefinedEntity : undefinedEntities) {
            String content = String.format(UNKNOWN_CONTENT, undefinedEntity.getId());
            Comment comment = asMatchedConcept(projectVersion, targetArtifact, CommentType.UNDEFINED_CONCEPT, content);

            CommentConcept commentConcept = new CommentConcept();
            commentConcept.setComment(comment);
            commentConcept.setConceptName(undefinedEntity.getId());

            conceptComments.add(commentConcept);
        }
        return conceptComments;
    }

    private <T, K> Map<T, List<CommentArtifact>> createCommentArtifactMap(
        ProjectVersion projectVersion,
        Artifact targetArtifact,
        Map<T, List<K>> group2concepts,
        Function<T, String> contentCreator,
        Function<K, Optional<Artifact>> artifactLookup,
        CommentType commentType) {
        Map<T, List<CommentArtifact>> id2artifacts = new HashMap<>();

        for (Map.Entry<T, List<K>> entry : group2concepts.entrySet()) {
            List<CommentArtifact> entryArtifacts = new ArrayList<>();
            String commentContent = contentCreator.apply(entry.getKey());
            Comment comment = asMatchedConcept(projectVersion, targetArtifact, commentType, commentContent);
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
            id2artifacts.put(entry.getKey(), entryArtifacts);
        }
        return id2artifacts;
    }

    /**
     * Creates comment of type MatchedConcept on given artifact.
     *
     * @param projectVersion Project version that comment is created in.
     * @param targetArtifact The artifact being commented on.
     * @return Base comment of type MatchedConcept.
     */
    private Comment asMatchedConcept(ProjectVersion projectVersion,
                                     Artifact targetArtifact,
                                     CommentType commentType,
                                     String content) {
        Comment comment = new Comment();
        comment.setStatus(CommentStatus.ACTIVE);
        comment.setType(commentType);
        comment.setContent(content);
        comment.setAuthor(null);// generated so no author
        comment.setVersion(projectVersion);
        comment.setArtifact(targetArtifact);
        return comment;
    }

    /**
     * Converts CommentMap to multi-artifact DTOs.
     *
     * @param saveCommentMap     Whether to save the comment map to the database.
     * @param commentArtifactMap Map of group to comment artifacts in that group.
     * @return List of MultiArtifact Comments.
     */
    private List<MultiArtifactCommentDTO> getMultiArtifactCommentDTOS(
        boolean saveCommentMap,
        Map<Integer, List<CommentArtifact>> commentArtifactMap) {
        if (saveCommentMap) {
            saveCommentArtifactMap(commentArtifactMap);
        }

        return mapToDTOs(commentArtifactMap, commentArtifacts -> {
            List<UUID> artifactIds = commentArtifacts
                .stream()
                .map(commentArtifact -> commentArtifact.getArtifactReferenced().getArtifactId())
                .toList();
            Comment comment = commentArtifacts.get(0).getComment();
            return MultiArtifactCommentDTO.fromComment(comment, artifactIds);
        });
    }

    /**
     * Converts list to a map grouping all concepts under single key or a concept per row.
     *
     * @param commentConcepts Concepts to group into map.
     * @param itemPerRow      If true, each concept is placed on a row by itself. Otherwise, all concepts are placed
     *                        together.
     * @param <K>             The type of object being placed.
     * @return Map of group to concepts in group.
     */
    @NotNull
    private <K> Map<Integer, List<K>> listToMap(List<K> commentConcepts, boolean itemPerRow) {
        Map<Integer, List<K>> hashMap = new HashMap<>();
        if (itemPerRow) {
            for (int i = 0; i < commentConcepts.size(); i++) {
                hashMap.put(i, commentConcepts.subList(i, i + 1));
            }
        } else {
            hashMap.put(0, commentConcepts);
        }

        return hashMap;
    }

    /**
     * Creates content of multi-concept match comment.
     *
     * @param conceptMatches List of matches.
     * @return Comment content.
     */
    private String createMultiMatchContent(List<ConceptMatchDTO> conceptMatches) {
        String concepts = String.join(",", conceptMatches.stream().map(ConceptMatchDTO::getId).toList());
        return String.format(MULTI_CONTENT, concepts);
    }
}
