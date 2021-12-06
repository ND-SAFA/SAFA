package edu.nd.crc.safa.server.services;

import java.util.Optional;

import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.server.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.TraceLinkVersionRepository;
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

    private final TraceLinkVersionRepository traceLinkVersionRepository;
    private final ArtifactRepository artifactRepository;

    @Autowired
    public TraceLinkService(TraceLinkVersionRepository traceLinkVersionRepository,
                            ArtifactRepository artifactRepository) {
        this.traceLinkVersionRepository = traceLinkVersionRepository;
        this.artifactRepository = artifactRepository;
    }

    public Pair<TraceAppEntity, String> parseTraceLink(ProjectVersion projectVersion,
                                                       String sourceName,
                                                       String targetName) {
        ArtifactFinder artifactFinder = (a) ->
            artifactRepository.findByProjectAndName(projectVersion.getProject(), a);
        return parseTraceLink(artifactFinder, this::queryForLinkBetween, sourceName,
            targetName);
    }

    public Pair<TraceAppEntity, String> parseTraceLink(ArtifactFinder artifactFinder,
                                                       TraceLinkFinder traceLinkFinder,
                                                       String sourceName,
                                                       String targetName) {
        String error = validateTraceLink(artifactFinder, traceLinkFinder, sourceName, targetName);
        if (error != null) {
            return new Pair<>(null, error);
        } else {
            TraceAppEntity trace = new TraceAppEntity(sourceName, targetName);
            return new Pair<>(trace, error);
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
        Optional<TraceLinkVersion> linkQuery = traceLinkFinder.findTrace(sourceArtifact, targetArtifact);
        if (linkQuery.isPresent()) {
            return "Trace link between source and target already exists";
        } else {
            return null;
        }
    }

    public Optional<TraceLinkVersion> queryForLinkBetween(Artifact sourceArtifact, Artifact targetArtifact) {
        Optional<TraceLinkVersion> traceQuery = this.traceLinkVersionRepository
            .getApprovedLinkIfExist(sourceArtifact, targetArtifact);
        if (traceQuery.isPresent()) {
            return traceQuery;
        }
        return this.traceLinkVersionRepository
            .getApprovedLinkIfExist(targetArtifact, sourceArtifact);
    }
}
