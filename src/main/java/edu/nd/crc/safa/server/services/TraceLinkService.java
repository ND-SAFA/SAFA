package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.server.db.entities.app.TraceApplicationEntity;
import edu.nd.crc.safa.server.db.entities.sql.ApplicationActivity;
import edu.nd.crc.safa.server.db.entities.sql.Artifact;
import edu.nd.crc.safa.server.db.entities.sql.ParserError;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.entities.sql.TraceLink;
import edu.nd.crc.safa.server.db.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.db.repositories.ParserErrorRepository;
import edu.nd.crc.safa.server.db.repositories.TraceLinkRepository;
import edu.nd.crc.safa.server.messages.ServerError;

import org.javatuples.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Responsible for providing an access to a project's
 * trace links.
 */
@Service
public class TraceLinkService {

    private final TraceLinkRepository traceLinkRepository;
    private final ArtifactRepository artifactRepository;
    private final ParserErrorRepository parserErrorRepository;
    private final RevisionNotificationService revisionNotificationService;

    @Autowired
    public TraceLinkService(TraceLinkRepository traceLinkRepository,
                            ArtifactRepository artifactRepository,
                            ParserErrorRepository parserErrorRepository,
                            RevisionNotificationService revisionNotificationService) {
        this.traceLinkRepository = traceLinkRepository;
        this.artifactRepository = artifactRepository;
        this.parserErrorRepository = parserErrorRepository;
        this.revisionNotificationService = revisionNotificationService;
    }

    public void createTraceLinks(ProjectVersion projectVersion, List<TraceApplicationEntity> traces)
        throws ServerError {
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
        this.revisionNotificationService.saveAndBroadcastTraceLinks(projectVersion.getProject(), newLinks);
        this.parserErrorRepository.saveAll(newErrors);
    }

    public Pair<TraceLink, ParserError> createTrace(ProjectVersion projectVersion,
                                                    TraceApplicationEntity t) {
        return createTrace(projectVersion, t.source, t.target);
    }

    public Pair<TraceLink, ParserError> createTrace(ProjectVersion projectVersion,
                                                    String sourceName,
                                                    String targetName) {
        Project project = projectVersion.getProject();
        Optional<Artifact> source = this.artifactRepository.findByProjectAndName(project, sourceName);
        if (!source.isPresent()) {
            ParserError sourceError = new ParserError(projectVersion,
                "Could not find source artifact: " + sourceName,
                ApplicationActivity.PARSING_TRACES);
            return new Pair<>(null, sourceError);
        }
        Optional<Artifact> target = this.artifactRepository.findByProjectAndName(project, targetName);
        if (!target.isPresent()) {
            ParserError targetError = new ParserError(projectVersion,
                "Could not find target artifact: " + targetName,
                ApplicationActivity.PARSING_TRACES);
            return new Pair<>(null, targetError);
        }
        // Check for already existing trace link
        Artifact sourceArtifact = source.get();
        Artifact targetArtifact = target.get();
        Optional<TraceLink> linkQuery = linkExists(sourceArtifact, targetArtifact);
        if (linkQuery.isPresent()) {
            ParserError targetError = new ParserError(projectVersion,
                "Trace link between source and target already exists",
                ApplicationActivity.PARSING_TRACES);
            return new Pair<>(null, targetError);
        } else {
            return new Pair<>(new TraceLink(sourceArtifact, targetArtifact), null);
        }
    }

    public Optional<TraceLink> linkExists(Artifact sourceArtifact, Artifact targetArtifact) {
        Optional<TraceLink> traceQuery = this.traceLinkRepository
            .getApprovedLinkIfExist(sourceArtifact, targetArtifact);
        if (traceQuery.isPresent()) {
            return traceQuery;
        }
        return this.traceLinkRepository
            .getApprovedLinkIfExist(targetArtifact, sourceArtifact);
    }
}
