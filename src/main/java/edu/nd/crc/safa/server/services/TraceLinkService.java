package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ParserError;
import edu.nd.crc.safa.server.entities.db.ProjectParsingActivities;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.ParserErrorRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.repositories.TraceLinkRepository;
import edu.nd.crc.safa.utilities.ArtifactFinder;
import edu.nd.crc.safa.utilities.TraceLinkFinder;

import org.javatuples.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Provides interface to validating and creating trace links.
 */
@Service
public class TraceLinkService {

    private final ProjectVersionRepository projectVersionRepository;
    private final TraceLinkRepository traceLinkRepository;
    private final ArtifactRepository artifactRepository;
    private final ParserErrorRepository parserErrorRepository;

    @Autowired
    public TraceLinkService(ProjectVersionRepository projectVersionRepository,
                            TraceLinkRepository traceLinkRepository,
                            ArtifactRepository artifactRepository,
                            ParserErrorRepository parserErrorRepository) {
        this.projectVersionRepository = projectVersionRepository;
        this.traceLinkRepository = traceLinkRepository;
        this.artifactRepository = artifactRepository;
        this.parserErrorRepository = parserErrorRepository;

    }

    public void createTraceLinks(ProjectVersion projectVersion, List<TraceAppEntity> traces) {
        List<TraceLink> newLinks = new ArrayList<>();
        List<ParserError> newErrors = new ArrayList<>();
        traces.forEach(t -> {
            Pair<TraceLink, ParserError> result = createTrace(projectVersion, t);
            if (result.getValue0() != null) {
                newLinks.add(result.getValue0());
            }
            if (result.getValue1() != null) {
                newErrors.add(result.getValue1());
            }
        });
        this.traceLinkRepository.saveAll(newLinks);
        this.parserErrorRepository.saveAll(newErrors);
    }

    public Pair<TraceLink, ParserError> createTrace(ProjectVersion projectVersion,
                                                    TraceAppEntity t) {
        ArtifactFinder artifactFinder = (a) ->
            artifactRepository.findByProjectAndName(projectVersion.getProject(), a);
        String sourceName = t.getSource();
        String targetName = t.getTarget();
        String error = validateTraceLink(artifactFinder, this::queryForLinkBetween, sourceName, targetName);

        if (error != null) {
            return new Pair<>(null, new ParserError(projectVersion, error,
                ProjectParsingActivities.PARSING_TRACES));
        } else {
            Artifact sourceArtifact = artifactFinder.findArtifact(sourceName).get(); // TODO: Fix warning
            Artifact targetArtifact = artifactFinder.findArtifact(targetName).get();
            TraceLink traceLink = new TraceLink(t);
            traceLink.setSourceArtifact(sourceArtifact);
            traceLink.setTargetArtifact(targetArtifact);
            return new Pair<>(traceLink, null);
        }
    }

    public Pair<TraceLink, String> createTrace(ProjectVersion projectVersion,
                                               String sourceName,
                                               String targetName) {
        ArtifactFinder artifactFinder = (a) ->
            artifactRepository.findByProjectAndName(projectVersion.getProject(), a);
        return parseTraceLink(artifactFinder, this::queryForLinkBetween, sourceName,
            targetName);
    }

    //TODO: FIX ambuiguity between validation and parsing
    public Pair<TraceLink, String> parseTraceLink(ArtifactFinder artifactFinder,
                                                  TraceLinkFinder traceLinkFinder,
                                                  String sourceName,
                                                  String targetName) {
        String error = validateTraceLink(artifactFinder, traceLinkFinder, sourceName, targetName);
        if (error != null) {
            return new Pair<>(null, error);
        } else {
            Artifact sourceArtifact = artifactFinder.findArtifact(sourceName).get(); // TODO: Fix warning
            Artifact targetArtifact = artifactFinder.findArtifact(targetName).get();
            return new Pair<>(new TraceLink(sourceArtifact, targetArtifact), error);
        }
    }

    public String validateTraceLink(ArtifactFinder artifactFinder,
                                    TraceLinkFinder traceLinkFinder,
                                    String sourceName,
                                    String targetName) {
        Optional<Artifact> source = artifactFinder.findArtifact(sourceName);
        if (source.isEmpty()) {
            return "Could not find source artifact: " + sourceName;
        }

        Optional<Artifact> target = artifactFinder.findArtifact(targetName);
        if (target.isEmpty()) {
            return "Could not find target artifact: " + targetName;
        }

        // Check for already existing trace link
        Artifact sourceArtifact = source.get();
        Artifact targetArtifact = target.get();
        Optional<TraceLink> linkQuery = traceLinkFinder.findTrace(sourceArtifact, targetArtifact);
        if (linkQuery.isPresent()) {
            return "Trace link between source and target already exists";
        } else {
            return null;
        }
    }

    public Optional<TraceLink> queryForLinkBetween(Artifact sourceArtifact, Artifact targetArtifact) {
        Optional<TraceLink> traceQuery = this.traceLinkRepository
            .getApprovedLinkIfExist(sourceArtifact, targetArtifact);
        if (traceQuery.isPresent()) {
            return traceQuery;
        }
        return this.traceLinkRepository
            .getApprovedLinkIfExist(targetArtifact, sourceArtifact);
    }

    /**
     * Creates a trace link between specified sourceId and target artifact ids at given version.
     *
     * @param projectVersion ProjectVersion that will be marked with the new trace link.
     * @param sourceId       UUID of source artifact.
     * @param targetId       UUID of target artifact.
     * @return TraceApplicationEntity representing the created entity.
     * @throws SafaError Throws error if either project version, source, or target artifact not found.
     */
    public ServerResponse createNewTraceLInk(ProjectVersion projectVersion,
                                             String sourceId,
                                             String targetId) throws SafaError {
        Pair<TraceLink, String> creationResponse = this.createTrace(projectVersion, sourceId,
            targetId);
        if (creationResponse.getValue1() != null) {
            String errorMessage = creationResponse.getValue1();
            throw new SafaError(errorMessage);
        }
        TraceLink traceLink = creationResponse.getValue0();
        this.traceLinkRepository.saveAll(List.of(traceLink));
        return new ServerResponse(new TraceAppEntity(traceLink));
    }

    /**
     * Retrieves the corresponding trace link in given version and updates information
     * to given application state.
     *
     * @param traceAppEntity The trace being updated.
     * @throws SafaError Throws error if version not found.
     */
    public void updateTraceLink(TraceAppEntity traceAppEntity) throws SafaError {
        TraceLink traceLink = getEntity(traceAppEntity);
        traceLink.setApprovalStatus(traceAppEntity.approvalStatus);
        this.traceLinkRepository.save(traceLink);
    }

    /**
     * Deletes trace link containing the same traceLinkID as given entity
     *
     * @param traceAppEntity The trace link deleted in application.
     * @throws SafaError Throws error is trace link with id not found.
     */
    public void deleteTraceLink(TraceAppEntity traceAppEntity) throws SafaError {
        TraceLink traceLink = getEntity(traceAppEntity);
        this.traceLinkRepository.delete(traceLink);
    }

    private TraceLink getEntity(TraceAppEntity traceAppEntity) throws SafaError {
        UUID traceLinkId = UUID.fromString(traceAppEntity.getTraceLinkId());
        Optional<TraceLink> traceLinkQuery =
            this.traceLinkRepository.findById(traceLinkId);
        if (traceLinkQuery.isEmpty()) {
            throw new SafaError("Could not find trace link with id:" + traceLinkId);
        }
        return traceLinkQuery.get();
    }
}
