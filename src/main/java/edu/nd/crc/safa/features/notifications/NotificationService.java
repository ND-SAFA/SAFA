package edu.nd.crc.safa.features.notifications;

import java.util.UUID;

import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.notifications.messages.LayoutMessage;
import edu.nd.crc.safa.features.notifications.messages.ProjectMessage;
import edu.nd.crc.safa.features.notifications.messages.VersionMessage;
import edu.nd.crc.safa.features.notifications.messages.layout.LayoutEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectEntityTypes;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.features.versions.entities.app.VersionEntityTypes;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Scope;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;

/**
 * Responsible for sending notifications to subscribers of certain topics.
 */
@Service
@Scope("singleton")
public class NotificationService {

    private final SimpMessagingTemplate messagingTemplate;
    private final SafaUserService safaUserService;

    @Autowired
    public NotificationService(SimpMessagingTemplate template, SafaUserService safaUserService) {
        this.messagingTemplate = template;
        this.safaUserService = safaUserService;
    }

    /**
     * Returns the topic endpoint for notifications to project entities.
     *
     * @param project The project whose topic is returned.
     * @return String representing path to project version endpoint.
     */
    public static String getProjectTopic(Project project) {
        return String.format("/topic/projects/%s", project.getProjectId().toString());
    }

    /**
     * Returns the topic endpoint for notifications to project version entities.
     *
     * @param projectVersion The project version whose topic is returned.
     * @return String representing path to project version endpoint.
     */
    public static String getVersionTopic(ProjectVersion projectVersion) {
        return String.format("/topic/revisions/%s", projectVersion.getVersionId());
    }

    /**
     * Returns the topic for receiving job updates for given job.
     *
     * @param jobDbEntity The job to subscribe to.
     * @return String representing job topic.
     */
    public static String getJobTopic(JobDbEntity jobDbEntity) {
        return String.format("/topic/jobs/%s", jobDbEntity.getId());
    }

    /**
     * Topic responsible for alerting users whenever a layout to a document has been changed.
     *
     * @param projectVersion The project version whose artifact positions have been changed.
     * @return String representing version layout topic.
     */
    public static String getProjectVersionLayoutTopic(ProjectVersion projectVersion) {
        return String.format("/topics/layout/document/%s", projectVersion.getVersionId().toString());
    }

    /**
     * Notifies all subscribers of given project to update the defined project entity.
     *
     * @param project            The project whose subscribers will be notified of update.
     * @param projectEntityTypes The project entities to update.
     */
    public void broadcastUpdateProjectMessage(Project project, ProjectEntityTypes projectEntityTypes) {
        SafaUser safaUser = this.safaUserService.getCurrentUser();
        String versionTopicDestination = getProjectTopic(project);
        ProjectMessage message = new ProjectMessage(safaUser.getEmail(), projectEntityTypes);
        messagingTemplate.convertAndSend(versionTopicDestination, message);
    }

    /**
     * Notifies all subscribers of given version to update the defined project entity.
     *
     * @param projectVersion     The version whose subscribers will be notified of update.
     * @param versionEntityTypes The versioned entities to update.
     */
    public void broadcastUpdateProjectVersionMessage(ProjectVersion projectVersion,
                                                     VersionEntityTypes versionEntityTypes) {
        SafaUser safaUser = this.safaUserService.getCurrentUser();
        String versionTopicDestination = getVersionTopic(projectVersion);
        VersionMessage message = new VersionMessage(safaUser.getEmail(), versionEntityTypes);
        messagingTemplate.convertAndSend(versionTopicDestination, message);
    }

    /**
     * Sends job to topic subscribers.
     *
     * @param jobDbEntity The job to broadcast.
     */
    public void broadcastUpdateJobMessage(JobDbEntity jobDbEntity) {
        String jobTopic = getJobTopic(jobDbEntity);
        JobAppEntity jobAppEntity = JobAppEntity.createFromJob(jobDbEntity);
        messagingTemplate.convertAndSend(jobTopic, jobAppEntity);
    }

    /**
     * Notifies subscribes that document layout has changed.
     *
     * @param projectVersion Project version whose artifact positions was updated.
     * @param documentId     Document ID of layout whose been updated.
     */
    public void broadcastDocumentLayoutMessage(ProjectVersion projectVersion,
                                               UUID documentId) {
        String layoutTopic = getProjectVersionLayoutTopic(projectVersion);
        LayoutMessage layoutMessage = new LayoutMessage(LayoutEntity.DOCUMENT, documentId);
        messagingTemplate.convertAndSend(layoutTopic, layoutMessage);
    }

    /**
     * Notifies subscribes that project layout has changed (e.g. generated entire layout or default document).
     *
     * @param projectVersion The version whose layout will be notified.
     */
    public void broadcastProjectLayoutMessage(ProjectVersion projectVersion) {
        String layoutTopic = getProjectVersionLayoutTopic(projectVersion);
        LayoutMessage layoutMessage = new LayoutMessage(LayoutEntity.PROJECT, null);
        messagingTemplate.convertAndSend(layoutTopic, layoutMessage);
    }
}
