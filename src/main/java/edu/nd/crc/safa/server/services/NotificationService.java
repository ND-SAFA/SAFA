package edu.nd.crc.safa.server.services;

import edu.nd.crc.safa.server.entities.app.ProjectMessage;
import edu.nd.crc.safa.server.entities.app.VersionMessage;
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

    public void broadUpdateProjectVersionMessage(ProjectVersion projectVersion,
                                                 VersionMessage versionMessage) {
        String versionTopicDestination = getVersionTopic(projectVersion);
        String message = versionMessage.toString();
        messagingTemplate.convertAndSend(versionTopicDestination, message);
    }

    public void broadUpdateProjectMessage(Project project, ProjectMessage projectMessage) {
        String versionTopicDestination = getProjectTopic(project);
        String message = projectMessage.toString();
        messagingTemplate.convertAndSend(versionTopicDestination, message);
    }
}
