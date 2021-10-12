package edu.nd.crc.safa.server.services;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.db.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.db.entities.app.TraceApplicationEntity;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.server.db.entities.sql.ModificationType;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.entities.sql.TraceLink;
import edu.nd.crc.safa.server.db.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.server.db.repositories.TraceLinkRepository;
import edu.nd.crc.safa.server.messages.ArtifactChange;
import edu.nd.crc.safa.server.messages.Revision;
import edu.nd.crc.safa.server.messages.ServerError;
import edu.nd.crc.safa.server.messages.TraceChange;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;

@Service
public class RevisionNotificationService {

    private final SimpMessagingTemplate template;
    private final ObjectMapper mapper;
    private final TraceLinkRepository traceLinkRepository;
    private final ArtifactBodyRepository artifactBodyRepository;

    @Autowired
    public RevisionNotificationService(SimpMessagingTemplate template,
                                       TraceLinkRepository traceLinkRepository,
                                       ArtifactBodyRepository artifactBodyRepository) {
        this.template = template;
        this.traceLinkRepository = traceLinkRepository;
        this.artifactBodyRepository = artifactBodyRepository;
        mapper = new ObjectMapper();
    }

    public void saveArtifactBodies(ProjectVersion projectVersion,
                                   List<ArtifactBody> artifactBodies) throws ServerError {
        artifactBodyRepository.saveAll(artifactBodies);

        Revision revision = new Revision();
        revision.setRevision(projectVersion.getRevision());
        List<ArtifactChange> artifactChanges =
            artifactBodies
                .stream()
                .map(aBody -> new ArtifactChange(ModificationType.MODIFIED, new ArtifactAppEntity(aBody)))
                .collect(Collectors.toList());
        revision.setArtifactChanges(artifactChanges);
        String revisionAsString;
        try {
            revisionAsString = mapper.writeValueAsString(revision);
        } catch (JsonProcessingException e) {
            throw new ServerError("Internal error occurred while serializing project revision.");
        }
        String versionTopicDestination = getVersionTopic(projectVersion);
        template.convertAndSend(versionTopicDestination, revisionAsString);
        System.out.println("BROADCASTING TO:" + versionTopicDestination);
    }

    public void saveAndBroadcastTraceLinks(Project project, List<TraceLink> traceLinks) throws ServerError {
        System.out.println("TRACE LINKS:" + traceLinks);
        traceLinkRepository.saveAll(traceLinks);
        Revision revision = new Revision();
        List<TraceChange> traceChanges =
            traceLinks
                .stream()
                .map(trace -> new TraceChange(ModificationType.ADDED, new TraceApplicationEntity(trace)))
                .collect(Collectors.toList());
        System.out.println("SENDING TRACE CHANGES:" + traceChanges);
        revision.setTraceChanges(traceChanges);
        String revisionAsString;
        try {
            revisionAsString = mapper.writeValueAsString(revision);
        } catch (JsonProcessingException e) {
            throw new ServerError("Internal error occurred while serializing project revision.");
        }
        String projectTopicDestination = getProjectTopic(project);
        template.convertAndSend(projectTopicDestination, revisionAsString);
        System.out.println("BROADCASTING TO:" + projectTopicDestination);
    }

    public String getVersionTopic(ProjectVersion projectVersion) {
        return String.format("/topic/revisions/%s", projectVersion.getVersionId());
    }

    public String getProjectTopic(Project project) {
        return String.format("/topic/projects/%s", project.getProjectId());
    }
}
