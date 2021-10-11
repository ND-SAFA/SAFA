package edu.nd.crc.safa.server.services;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.db.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.db.entities.app.TraceApplicationEntity;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.server.db.entities.sql.ModificationType;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.entities.sql.TraceLink;
import edu.nd.crc.safa.server.db.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.server.db.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.db.repositories.TraceLinkRepository;
import edu.nd.crc.safa.server.messages.ArtifactChange;
import edu.nd.crc.safa.server.messages.Revision;
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
    private final ProjectVersionRepository projectVersionRepository;
    private final ArtifactRepository artifactRepository;
    private final TraceLinkRepository traceLinkRepository;
    private final ArtifactBodyRepository artifactBodyRepository;

    @Autowired
    public RevisionNotificationService(SimpMessagingTemplate template,
                                       ProjectVersionRepository projectVersionRepository,
                                       ArtifactRepository artifactRepository,
                                       TraceLinkRepository traceLinkRepository,
                                       ArtifactBodyRepository artifactBodyRepository) {
        this.template = template;
        this.projectVersionRepository = projectVersionRepository;
        this.artifactRepository = artifactRepository;
        this.traceLinkRepository = traceLinkRepository;
        this.artifactBodyRepository = artifactBodyRepository;
        mapper = new ObjectMapper();
    }

    public void saveAndNotify(List<ArtifactBody> artifactBodies,
                              List<TraceLink> traceLinks,
                              ProjectVersion projectVersion) throws JsonProcessingException {
        artifactBodyRepository.saveAll(artifactBodies);

        Revision revision = new Revision();
        revision.setRevision(projectVersion.getRevision() + 1);
        List<ArtifactChange> artifactChanges =
            artifactBodies
                .stream()
                .map(aBody -> new ArtifactChange(ModificationType.MODIFIED, new ArtifactAppEntity(aBody)))
                .collect(Collectors.toList());
        List<TraceChange> traceChanges =
            traceLinks
                .stream()
                .map(trace -> new TraceChange(ModificationType.ADDED, new TraceApplicationEntity(trace)))
                .collect(Collectors.toList());
        revision.setArtifactChanges(artifactChanges);
        revision.setTraceChanges(traceChanges);
        String revisionAsString = mapper.writeValueAsString(revision);
        template.convertAndSend(getVersionTopic(projectVersion), revisionAsString);
    }

    public String getVersionTopic(ProjectVersion projectVersion) {
        return String.format("/topic/revisions/%s", projectVersion.getVersionId());
    }
}
