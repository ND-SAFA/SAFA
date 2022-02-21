package edu.nd.crc.safa.server.services;

import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.entities.app.ProjectEntities;
import edu.nd.crc.safa.server.entities.app.ProjectMessage;
import edu.nd.crc.safa.server.entities.app.VersionMessage;
import edu.nd.crc.safa.server.entities.app.VersionedEntities;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.SafaUser;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;

/**
 * Responsible for sending notifications to subscribers of certain topics.
 */
@Service
public class NotificationService {

    private final SimpMessagingTemplate messagingTemplate;
    private final SafaUserService safaUserService;

    @Autowired
    public NotificationService(SimpMessagingTemplate template, SafaUserService safaUserService) {
        this.messagingTemplate = template;
        this.safaUserService = safaUserService;
    }

    public static String getProjectTopic(Project project) {
        return String.format("/topic/projects/%s", project.getProjectId().toString());
    }

    public static String getVersionTopic(ProjectVersion projectVersion) {
        return String.format("/topic/revisions/%s", projectVersion.getVersionId());
    }

    /**
     * Notifies all subscribers of given version to update the defined project entity.
     *
     * @param projectVersion    The version whose subscribers will be notified of update.
     * @param versionedEntities The versioned entities to update.
     */
    public void broadUpdateProjectVersionMessage(ProjectVersion projectVersion,
                                                 VersionedEntities versionedEntities) {
        SafaUser safaUser = this.safaUserService.getCurrentUser();
        String versionTopicDestination = getVersionTopic(projectVersion);
        VersionMessage message = new VersionMessage(safaUser.getEmail(), versionedEntities);
        messagingTemplate.convertAndSend(versionTopicDestination, message);
    }

    /**
     * Notifies all subscribers of given project to update the defined project entity.
     *
     * @param project         The project whose subscribers will be notified of update.
     * @param projectEntities The project entities to update.
     */
    public void broadUpdateProjectMessage(Project project, ProjectEntities projectEntities) {
        SafaUser safaUser = this.safaUserService.getCurrentUser();
        String versionTopicDestination = getProjectTopic(project);
        ProjectMessage message = new ProjectMessage(safaUser.getEmail(), projectEntities);
        messagingTemplate.convertAndSend(versionTopicDestination, message);
    }
}
