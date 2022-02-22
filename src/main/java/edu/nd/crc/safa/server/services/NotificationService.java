package edu.nd.crc.safa.server.services;

import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.entities.app.ProjectEntityTypes;
import edu.nd.crc.safa.server.entities.app.ProjectMessage;
import edu.nd.crc.safa.server.entities.app.VersionEntityTypes;
import edu.nd.crc.safa.server.entities.app.VersionMessage;
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
     * @param projectVersion     The version whose subscribers will be notified of update.
     * @param versionEntityTypes The versioned entities to update.
     */
    public void broadUpdateProjectVersionMessage(ProjectVersion projectVersion,
                                                 VersionEntityTypes versionEntityTypes) {
        SafaUser safaUser = this.safaUserService.getCurrentUser();
        String versionTopicDestination = getVersionTopic(projectVersion);
        VersionMessage message = new VersionMessage(safaUser.getEmail(), versionEntityTypes);
        messagingTemplate.convertAndSend(versionTopicDestination, message);
    }

    /**
     * Notifies all subscribers of given project to update the defined project entity.
     *
     * @param project            The project whose subscribers will be notified of update.
     * @param projectEntityTypes The project entities to update.
     */
    public void broadUpdateProjectMessage(Project project, ProjectEntityTypes projectEntityTypes) {
        SafaUser safaUser = this.safaUserService.getCurrentUser();
        String versionTopicDestination = getProjectTopic(project);
        ProjectMessage message = new ProjectMessage(safaUser.getEmail(), projectEntityTypes);
        messagingTemplate.convertAndSend(versionTopicDestination, message);
    }
}
