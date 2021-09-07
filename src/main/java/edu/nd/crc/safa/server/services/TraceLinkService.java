package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.db.entities.app.TraceApplicationEntity;
import edu.nd.crc.safa.db.entities.sql.ApplicationActivity;
import edu.nd.crc.safa.db.entities.sql.Artifact;
import edu.nd.crc.safa.db.entities.sql.ParserError;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.db.entities.sql.TraceLink;
import edu.nd.crc.safa.db.repositories.ArtifactRepository;
import edu.nd.crc.safa.db.repositories.ParserErrorRepository;
import edu.nd.crc.safa.db.repositories.TraceLinkRepository;

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

    @Autowired
    public TraceLinkService(TraceLinkRepository traceLinkRepository,
                            ArtifactRepository artifactRepository,
                            ParserErrorRepository parserErrorRepository) {
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
        TraceLink traceLink = new TraceLink(source.get(), target.get());
        return new Pair<>(traceLink, null);
    }
}
