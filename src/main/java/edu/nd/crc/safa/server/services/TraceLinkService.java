package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.server.entities.app.TraceApplicationEntity;
import edu.nd.crc.safa.server.entities.db.ApplicationActivity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ParserError;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.ParserErrorRepository;
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

    private final TraceLinkRepository traceLinkRepository;
    private final ArtifactRepository artifactRepository;
    private final ParserErrorRepository parserErrorRepository;

    @Autowired
    public TraceLinkService(TraceLinkRepository traceLinkRepository,
                            ArtifactRepository artifactRepository,
                            ParserErrorRepository parserErrorRepository,
                            RevisionNotificationService revisionNotificationService) {
        this.traceLinkRepository = traceLinkRepository;
        this.artifactRepository = artifactRepository;
        this.parserErrorRepository = parserErrorRepository;
    }

    public void createTraceLinks(ProjectVersion projectVersion, List<TraceApplicationEntity> traces) {
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
                                                    TraceApplicationEntity t) {
        ArtifactFinder artifactFinder = (a) ->
            artifactRepository.findByProjectAndName(projectVersion.getProject(), a);
        String sourceName = t.getSource();
        String targetName = t.getTarget();
        String error = validateTraceLink(artifactFinder, this::queryForLinkBetween, sourceName, targetName);

        if (error != null) {
            return new Pair<>(null, new ParserError(projectVersion, error,
                ApplicationActivity.PARSING_TRACES));
        } else {
            Artifact sourceArtifact = artifactFinder.findArtifact(sourceName).get(); // TODO: Fix warning
            Artifact targetArtifact = artifactFinder.findArtifact(targetName).get();
            TraceLink traceLink = new TraceLink(t);
            traceLink.setSourceArtifact(sourceArtifact);
            traceLink.setTargetArtifact(targetArtifact);
            return new Pair<>(traceLink, null);
        }
    }

    public Pair<TraceLink, ParserError> createTrace(ProjectVersion projectVersion,
                                                    String sourceName,
                                                    String targetName) {
        ArtifactFinder artifactFinder = (a) ->
            artifactRepository.findByProjectAndName(projectVersion.getProject(), a);
        Pair<TraceLink, String> parseResponse = parseTraceLink(artifactFinder, this::queryForLinkBetween, sourceName,
            targetName);
        return new Pair<>(parseResponse.getValue0(), new ParserError(projectVersion, parseResponse.getValue1(),
            ApplicationActivity.PARSING_TRACES));
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
}
