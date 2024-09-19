package edu.nd.crc.safa.features.health;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
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
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.generation.common.GenerationLink;
import edu.nd.crc.safa.features.health.entities.ConceptMatchDTO;
import edu.nd.crc.safa.features.health.entities.HealthResponseDTO;
import edu.nd.crc.safa.features.health.entities.gen.GenContradiction;
import edu.nd.crc.safa.features.health.entities.gen.GenHealthResponse;
import edu.nd.crc.safa.features.health.entities.gen.GenUndefinedEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

import lombok.AllArgsConstructor;
import org.jetbrains.annotations.NotNull;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class HealthResponseSaver {
    private static final Logger logger = LoggerFactory.getLogger(HealthResponseSaver.class);

    private static final String UNKNOWN_CONTENT = "`%s` is used in artifact but undefined in project concepts.";
    private static final String MULTI_CONTENT = "Found multiple, conflicting concepts matching in artifact: %s";
    private static final String PREDICTED_CONTENT = "The concept `%s` was predicted to be used within the artifact.";
    private static final String CITED_CONTENT = "`%s` was cited in artifact.";
    private CommitService commitService;
    private CommentRepository commentRepository;
    private CommentArtifactRepository commentArtifactRepository;
    private CommentConceptRepository commentConceptRepository;
    private ArtifactRepository artifactRepository;

    /**
     * Saves health checks as comments under artifact.
     *
     * @param user           The user tagged with changing these entities.
     * @param projectVersion Project version to save comments under.
     * @param genResponse    GEN API response containing health checks.
     * @return Response object containing comments.
     */
    @NotNull
    public HealthResponseDTO saveHealthChecks(
        SafaUser user,
        HealthResponseDTO response,
        ProjectVersion projectVersion,
        GenHealthResponse genResponse
    ) {
        List<Artifact> projectArtifacts = artifactRepository.getProjectArtifacts(projectVersion.getProject().getId());
        Map<String, Artifact> artifactNameLookup = ProjectDataStructures.createEntityLookup(
            projectArtifacts,
            Artifact::getName
        );
        // save undefined entities
        response.addHealthChecks(
            saveUndefinedEntities(
                projectVersion, genResponse.getUndefinedConcepts(), artifactNameLookup
            )
        );
        // save contradictions
        response.addHealthChecks(
            saveContradictions(projectVersion, artifactNameLookup, genResponse.getContradictions())
        );

        // save direct matches as links
        response.addHealthChecks(
            saveDirectMatches(
                projectVersion,
                artifactNameLookup,
                genResponse.getDirectMatches()
            )
        );
        // save multi-matches as warning
        response.addHealthChecks(
            saveMultiMatchedConcepts(
                projectVersion, genResponse.getMultiMatches(), artifactNameLookup
            )
        );
        // save predicted matches as
        response.addHealthChecks(
            savePredictedMatches(
                projectVersion, genResponse.getPredictedMatches(), artifactNameLookup
            )
        );

        ProjectCommitDefinition commitDefinition = saveConceptLinks(
            projectVersion,
            genResponse.getPredictedMatches(),
            genResponse.getDirectMatches()
        );
        commitService.performCommit(commitDefinition, user);

        return response;
    }

    /**
     * Saves links from concept to target artifacts.
     *
     * @param projectVersion   The project version of the artifacts to link.
     * @param predictedMatches The list of predicted concept matches.
     * @param directMatches    List of direct matches found.
     * @return Project Commit Definition containing traces being added.
     */
    private ProjectCommitDefinition saveConceptLinks(ProjectVersion projectVersion,
                                                     List<GenerationLink> predictedMatches,
                                                     List<ConceptMatchDTO> directMatches) {
        List<TraceAppEntity> predictedLinks = predictedMatches.stream().map(GenerationLink::toTrace).toList();
        List<TraceAppEntity> manualLinks = directMatches.stream().map(t -> t.toTrace()).toList();
        ProjectCommitAppEntity projectCommitAppEntity = new ProjectCommitAppEntity();
        projectCommitAppEntity.getTraces().getAdded().addAll(predictedLinks);
        projectCommitAppEntity.getTraces().getAdded().addAll(manualLinks);

        ProjectCommitDefinition projectCommitDefinition = new ProjectCommitDefinition(projectCommitAppEntity);
        projectCommitDefinition.setCommitVersion(projectVersion);

        return projectCommitDefinition;
    }

    /**
     * Creates concept comments for each direct match found.
     *
     * @param projectVersion     The project version this comment was created in.
     * @param artifactNameLookup Map of name to artifact.
     * @param directMatches      The direct matches to create comments for.
     * @return List of concepts comments generated for artifact.
     */
    private List<ArtifactCommentDTO> saveDirectMatches(ProjectVersion projectVersion,
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
    private List<ArtifactCommentDTO> savePredictedMatches(ProjectVersion projectVersion,
                                                          List<GenerationLink> predictedConceptLinks,
                                                          Map<String, Artifact> artifactNameLookup) {

        List<CommentArtifact> commentArtifactsToSave = new ArrayList<>();
        for (GenerationLink generationLink : predictedConceptLinks) {
            Artifact artifact = artifactNameLookup.get(generationLink.getSource());
            Artifact conceptReferenced = artifactNameLookup.get(generationLink.getTarget());
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
    private List<MultiArtifactCommentDTO> saveMultiMatchedConcepts(
        ProjectVersion projectVersion,
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
    private List<UndefinedConceptCommentDTO> saveUndefinedEntities(ProjectVersion projectVersion,
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
                    undefinedEntity.getDefinition()
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
    private List<MultiArtifactCommentDTO> saveContradictions(ProjectVersion projectVersion,
                                                             Map<String, Artifact> artifactNameLookup,
                                                             List<GenContradiction> contradictions) {
        Map<Comment, List<CommentArtifact>> comment2contradictions = new HashMap<>();
        for (GenContradiction contradiction : contradictions) {
            String ownerArtifactId = contradiction.getConflictingIds().get(0);
            contradiction.getConflictingIds().remove(0);
            Artifact artifact = artifactNameLookup.get(ownerArtifactId);
            Comment comment = asMatchedConcept(
                projectVersion,
                artifact,
                CommentType.CONTRADICTION,
                contradiction.getExplanation()
            );
            comment = this.commentRepository.save(comment);

            for (String artifactId : contradiction.getConflictingIds()) {
                if (artifactId.equals(ownerArtifactId)) {
                    continue;
                }
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
        String explanation = link.getExplanation();
        if (explanation == null || explanation.isBlank()) {
            return String.format(PREDICTED_CONTENT, link.getTarget());
        }
        return explanation;
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
