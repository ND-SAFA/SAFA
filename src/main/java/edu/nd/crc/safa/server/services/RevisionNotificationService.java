package edu.nd.crc.safa.server.services;

import edu.nd.crc.safa.server.entities.api.ProjectWebSocketMessage;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;

@Service
public class RevisionNotificationService {

    private final SimpMessagingTemplate messagingTemplate;

    @Autowired
    public RevisionNotificationService(SimpMessagingTemplate template) {
        this.messagingTemplate = template;
    }

    public static String getVersionTopic(ProjectVersion projectVersion) {
        return String.format("/topic/revisions/%s", projectVersion.getVersionId());
    }

    public void broadcastUpdateProject(ProjectVersion projectVersion) {
        String versionTopicDestination = getVersionTopic(projectVersion);
        ProjectWebSocketMessage update = new ProjectWebSocketMessage("excluded");
        messagingTemplate.convertAndSend(versionTopicDestination, update);
    }
}
