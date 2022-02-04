package edu.nd.crc.safa.server.services;

import edu.nd.crc.safa.server.entities.api.ProjectWebSocketMessage;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;

/**
 * Responsible for sending notifications to subscribers of certain topics.
 */
@Service
public class NotificationService {

    private final SimpMessagingTemplate messagingTemplate;

    @Autowired
    public NotificationService(SimpMessagingTemplate template) {
        this.messagingTemplate = template;
    }

    public static String getProjectTopic(Project project) {
        return String.format("/topic/projects/%s", project.getProjectId().toString());
    }

    public static String getVersionTopic(ProjectVersion projectVersion) {
        return String.format("/topic/revisions/%s", projectVersion.getVersionId());
    }

    public void broadUpdateProjectVersionMessage(ProjectVersion projectVersion) {
        String versionTopicDestination = getVersionTopic(projectVersion);
        ProjectWebSocketMessage update = new ProjectWebSocketMessage("excluded");
        messagingTemplate.convertAndSend(versionTopicDestination, update);
    }

    public void broadUpdateProjectMessage(Project project, String message) {
        String versionTopicDestination = getProjectTopic(project);
        ProjectWebSocketMessage update = new ProjectWebSocketMessage(message);
        messagingTemplate.convertAndSend(versionTopicDestination, update);
    }
}
