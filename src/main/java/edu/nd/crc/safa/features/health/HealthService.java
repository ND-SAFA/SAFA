package edu.nd.crc.safa.features.health;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
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
import edu.nd.crc.safa.features.health.entities.gen.GenContradiction;
import edu.nd.crc.safa.features.health.entities.gen.GenHealthResponse;
import edu.nd.crc.safa.features.health.entities.gen.GenUndefinedEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

import lombok.AllArgsConstructor;
import org.jetbrains.annotations.NotNull;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class HealthService {
    private static final Logger logger = LoggerFactory.getLogger(HealthService.class);
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
     * @param artifacts      Set of artifacts performing health checks for.
     * @return Response containing health checks.
     */
    public HealthResponseDTO performArtifactHealthChecks(ProjectVersion projectVersion,
                                                         List<ArtifactAppEntity> artifacts) {
        List<Artifact> projectArtifacts = artifactRepository.getProjectArtifacts(projectVersion.getProject().getId());
        GenHealthResponse genResponse = generateHealthChecks(projectVersion, artifacts);
        HealthResponseDTO response = saveHealthChecks(projectVersion, projectArtifacts, genResponse);
        List<UUID> artifactIds = artifacts.stream().map(ArtifactAppEntity::getId).toList();
        return response.filterById(artifactIds);
    }

    /**
     * Calls GEN API to generate health checks.
     *
     * @param projectVersion  Project version used to retrieve artifact content.
     * @param targetArtifacts Target artifact being checks.
     * @return GEN response.
     */
    private GenHealthResponse generateHealthChecks(ProjectVersion projectVersion, List<ArtifactAppEntity> targetArtifacts) {
        List<GenerationArtifact> artifacts = artifactService
            .getAppEntities(projectVersion).stream().map(GenerationArtifact::new).collect(Collectors.toList());
        List<GenerationArtifact> targetGenArtifacts = targetArtifacts
            .stream()
            .map(GenerationArtifact::new)
            .toList();
        return genApi.generateHealthChecks(artifacts, targetGenArtifacts);
    }

    /**
     * Saves health checks as comments under artifact.
     *
     * @param projectVersion   Project version to save comments under.
     * @param projectArtifacts Artifacts in the project.
     * @param genResponse      GEN API response containing health checks.
     * @return Response object containing comments.
     */
    @NotNull
    private HealthResponseDTO saveHealthChecks(ProjectVersion projectVersion,
                                               List<Artifact> projectArtifacts,
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
                artifactNameLookup,
                genConceptResponse.getMatches()
            )
        );
        // save multi-matches as warning
        response.addHealthChecks(
            saveMultiMatchedConcepts(
                projectVersion, genConceptResponse.getMultiMatches(), artifactNameLookup
            )
        );
        // save predicted matches as
        response.addHealthChecks(
            savePredictedMatches(
                projectVersion, genConceptResponse.getPredictedMatches(), artifactNameLookup
            )
        );
        // save undefined entities
        response.addHealthChecks(
            saveUndefinedEntities(
                projectVersion, genConceptResponse.getUndefinedEntities(), artifactNameLookup
            )
        );
        // save contradictions
        response.addHealthChecks(
            saveContradictions(projectVersion, artifactNameLookup, genResponse.getContradictions())
        );
        return response;
    }

    /**
     * Creates concept comments for each direct match found.
     *
     * @param projectVersion     The project version this comment was created in.
     * @param artifactNameLookup Map of name to artifact.
     * @param directMatches      The direct matches to create comments for.
     * @return List of concepts comments generated for artifact.
     */
    public List<ArtifactCommentDTO> saveDirectMatches(ProjectVersion projectVersion,
                                                      Map<String, Artifact> artifactNameLookup,
                                                      List<ConceptMatchDTO> directMatches) {
        List<Comment> commentsToSave = new ArrayList<>();
        List<CommentArtifact> commentArtifactsToSave = new ArrayList<>();
        for (ConceptMatchDTO conceptMatchDTO : directMatches) {
            Artifact artifact = artifactNameLookup.get(conceptMatchDTO.getArtifactId());
            Artifact conceptReferenced = artifactNameLookup.get(conceptMatchDTO.getConceptId());
            Comment comment = asMatchedConcept(
                projectVersion,
                artifact,
                CommentType.CITED_CONCEPT,
                String.format(CITED_CONTENT, conceptMatchDTO.getConceptId())
            );
            comment = this.commentRepository.save(comment);
            CommentArtifact commentArtifact = new CommentArtifact(comment, conceptReferenced);
            commentArtifact = this.commentArtifactRepository.save(commentArtifact);
            commentsToSave.add(comment);
            commentArtifactsToSave.add(commentArtifact);
        }

        return commentArtifactsToSave.stream().map(ArtifactCommentDTO::fromComment).toList();
    }

    /**
     * Saves predicted links as comment suggestions.
     *
     * @param projectVersion        The project version to create comment in.
     * @param predictedConceptLinks List of predicted artifacts.
     * @param artifactNameLookup    Map of name to artifact.
     * @return List of comments DTOs.
     */
    public List<ArtifactCommentDTO> savePredictedMatches(ProjectVersion projectVersion,
                                                         List<GenerationLink> predictedConceptLinks,
                                                         Map<String, Artifact> artifactNameLookup) {
        List<CommentArtifact> commentArtifactsToSave = new ArrayList<>();
        for (GenerationLink generationLink : predictedConceptLinks) {
            Artifact artifact = artifactNameLookup.get(generationLink.getTarget());
            Artifact conceptReferenced = artifactNameLookup.get(generationLink.getSource());
            if (artifact == null || conceptReferenced == null) {
                String msg = String.format("One of these is undefined: Artifact(%s) Concept(%s)", artifact,
                    conceptReferenced);
                logger.info(msg);
                continue;
            }
            String commentContent = generatePredictionContent(generationLink);
            Comment comment = asMatchedConcept(
                projectVersion,
                artifact,
                CommentType.PREDICTED_CONCEPT,
                commentContent
            );
            comment = this.commentRepository.save(comment);
            CommentArtifact commentArtifact = new CommentArtifact(comment, conceptReferenced);
            commentArtifact = this.commentArtifactRepository.save(commentArtifact);
            commentArtifactsToSave.add(commentArtifact);
        }

        return commentArtifactsToSave.stream().map(ArtifactCommentDTO::fromComment).toList();
    }

    /**
     * Saves each group of matched concepts to the database and creates their representation.
     *
     * @param projectVersion     Project version the comment is created in.
     * @param multiMatches       Map containing groups of concept matches.
     * @param artifactNameLookup Map of artifact name to artifact entity.
     * @return List of DTOs.
     */
    public List<MultiArtifactCommentDTO> saveMultiMatchedConcepts(ProjectVersion projectVersion,
                                                                  Map<String, Map<Integer, List<ConceptMatchDTO>>> multiMatches,
                                                                  Map<String, Artifact> artifactNameLookup) {
        Map<Comment, List<CommentArtifact>> comment2commentArtifacts = new HashMap<>();
        for (Map.Entry<String, Map<Integer, List<ConceptMatchDTO>>> entry : multiMatches.entrySet()) {
            Artifact artifact = artifactNameLookup.get(entry.getKey());
            for (Map.Entry<Integer, List<ConceptMatchDTO>> artifactMultiMatches : entry.getValue().entrySet()) {
                String commentContent = createMultiMatchContent(artifactMultiMatches.getValue());
                Comment comment = asMatchedConcept(
                    projectVersion,
                    artifact,
                    CommentType.MULTI_MATCHED_CONCEPT,
                    commentContent
                );
                comment = this.commentRepository.save(comment);
                List<CommentArtifact> commentArtifactsLocal = new ArrayList<>();


                for (ConceptMatchDTO conceptMatchDTO : artifactMultiMatches.getValue()) {
                    Artifact conceptReferenced = artifactNameLookup.get(conceptMatchDTO.getConceptId());
                    CommentArtifact commentArtifact = new CommentArtifact(comment, conceptReferenced);
                    commentArtifact = this.commentArtifactRepository.save(commentArtifact);
                    commentArtifactsLocal.add(commentArtifact);
                }

                comment2commentArtifacts.put(comment, commentArtifactsLocal);
            }
        }

        return comment2commentArtifacts.entrySet().stream().map(dtoEntry -> {
            List<UUID> artifactIds = dtoEntry
                .getValue()
                .stream()
                .map(ca -> ca.getArtifactReferenced().getArtifactId())
                .toList();
            return MultiArtifactCommentDTO.fromComment(dtoEntry.getKey(), artifactIds);
        }).toList();
    }

    /**
     * Saves undefined entities as concept comments.
     *
     * @param projectVersion     The project version this comment is created in.
     * @param undefinedEntities  List of undefined entities in target artifact.
     * @param artifactNameLookup Artifact lookup table indexed by artifact name.
     * @return List of DTOS.
     */
    public List<UndefinedConceptCommentDTO> saveUndefinedEntities(ProjectVersion projectVersion,
                                                                  List<GenUndefinedEntity> undefinedEntities,
                                                                  Map<String, Artifact> artifactNameLookup) {
        List<CommentConcept> commentConceptsToSave = new ArrayList<>();

        for (GenUndefinedEntity undefinedEntity : undefinedEntities) {

            for (String artifactId : undefinedEntity.getArtifactIds()) {
                Artifact artifact = artifactNameLookup.get(artifactId);
                Comment comment = asMatchedConcept(
                    projectVersion,
                    artifact,
                    CommentType.UNDEFINED_CONCEPT,
                    undefinedEntity.getConceptDefinition()
                );
                comment = this.commentRepository.save(comment);
                CommentConcept commentConcept = new CommentConcept(
                    comment,
                    undefinedEntity.getConceptId()
                );
                commentConcept = this.commentConceptRepository.save(commentConcept);
                commentConceptsToSave.add(commentConcept);
            }
        }

        return commentConceptsToSave.stream().map(UndefinedConceptCommentDTO::fromComment).toList();
    }

    /**
     * Saves contradictions found in gen response.
     *
     * @param projectVersion     Project version used to save comment under.
     * @param artifactNameLookup Artifact Lookup table indexed by name.
     * @param contradictions     Gen Response.
     * @return List of multi-artifact DTOs.
     */
    public List<MultiArtifactCommentDTO> saveContradictions(ProjectVersion projectVersion,
                                                            Map<String, Artifact> artifactNameLookup,
                                                            List<GenContradiction> contradictions) {
        Map<Comment, List<CommentArtifact>> comment2contradictions = new HashMap<>();
        for (GenContradiction contradiction : contradictions) {
            for (String artifactId : contradiction.getConflictingIds()) {
                Artifact artifact = artifactNameLookup.get(artifactId);
                Comment comment = asMatchedConcept(
                    projectVersion,
                    artifact,
                    CommentType.CONTRADICTION,
                    contradiction.getExplanation()
                );
                comment = this.commentRepository.save(comment);

                List<CommentArtifact> artifactContradictions = new ArrayList<>();
                for (String conflictingArtifactId : contradiction.getConflictingIds()) {
                    Artifact otherConflictingArtifact = artifactNameLookup.get(conflictingArtifactId);
                    CommentArtifact commentArtifact = new CommentArtifact(
                        comment,
                        otherConflictingArtifact
                    );
                    commentArtifact = this.commentArtifactRepository.save(commentArtifact);
                    artifactContradictions.add(commentArtifact);
                }
                comment2contradictions.put(comment, artifactContradictions);
            }
        }

        return comment2contradictions.entrySet().stream().map(entry -> {
            List<UUID> artifactIds =
                entry.getValue().stream().map(ca -> ca.getArtifactReferenced().getArtifactId()).toList();
            return MultiArtifactCommentDTO.fromComment(entry.getKey(), artifactIds);
        }).toList();
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
     * Creates comment of type MatchedConcept on given artifact.
     *
     * @param projectVersion Project version that comment is created in.
     * @param owningArtifact The artifact being commented on.
     * @return Base comment of type MatchedConcept.
     */
    private Comment asMatchedConcept(ProjectVersion projectVersion,
                                     Artifact owningArtifact,
                                     CommentType commentType,
                                     String content) {
        Comment comment = new Comment();
        comment.setId(UUID.randomUUID());
        comment.setStatus(CommentStatus.ACTIVE);
        comment.setType(commentType);
        comment.setContent(content);
        comment.setAuthor(null);// generated so no author
        comment.setVersion(projectVersion);
        comment.setArtifact(owningArtifact);
        return comment;
    }

    /**
     * Creates content of multi-concept match comment.
     *
     * @param conceptMatches List of matches.
     * @return Comment content.
     */
    private String createMultiMatchContent(List<ConceptMatchDTO> conceptMatches) {
        String concepts = String.join(",", conceptMatches.stream().map(ConceptMatchDTO::getConceptId).toList());
        return String.format(MULTI_CONTENT, concepts);
    }
}
