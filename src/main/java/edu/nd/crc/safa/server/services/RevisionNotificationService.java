package edu.nd.crc.safa.server.services;

import java.util.List;

import edu.nd.crc.safa.server.db.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.db.entities.app.TraceApplicationEntity;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.messages.Update;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;

@Service
public class RevisionNotificationService {

    private final SimpMessagingTemplate messagingTemplate;
    private final ProjectVersionRepository projectVersionRepository;

    @Autowired
    public RevisionNotificationService(SimpMessagingTemplate template,
                                       ProjectVersionRepository projectVersionRepository) {
        this.messagingTemplate = template;
        this.projectVersionRepository = projectVersionRepository;
    }

    public static String getVersionTopic(ProjectVersion projectVersion) {
        return String.format("/topic/revisions/%s", projectVersion.getVersionId());
    }

    public static String getProjectTopic(Project project) {
        return String.format("/topic/projects/%s", project.getProjectId());
    }

    public void broadcastUpdateProject(ProjectVersion projectVersion) {
        String versionTopicDestination = getVersionTopic(projectVersion);
        Update update = new Update("excluded");
        messagingTemplate.convertAndSend(versionTopicDestination, update);
    }

    public void broadcastArtifact(ProjectVersion projectVersion, ArtifactAppEntity artifact) {
        String versionTopicDestination = getVersionTopic(projectVersion);
        Update update = new Update("included");
        update.setArtifacts(List.of(artifact));
        messagingTemplate.convertAndSend(versionTopicDestination, update);
    }

    public void broadcastTrace(Project project, TraceApplicationEntity trace) {
        List<ProjectVersion> projectVersions = projectVersionRepository.findByProject(project);
        Update update = new Update("included");
        update.setTraces(List.of(trace));
        for (ProjectVersion projectVersion : projectVersions) {
            String versionTopicDestination = getVersionTopic(projectVersion);
            messagingTemplate.convertAndSend(versionTopicDestination, update);
        }
    }
}
