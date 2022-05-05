package edu.nd.crc.safa.server.services;

import javax.annotation.PostConstruct;

import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.entities.app.project.ProjectEntityTypes;
import edu.nd.crc.safa.server.entities.app.project.ProjectMessage;
import edu.nd.crc.safa.server.entities.app.project.VersionEntityTypes;
import edu.nd.crc.safa.server.entities.app.project.VersionMessage;
import edu.nd.crc.safa.server.entities.db.Job;
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

    private static NotificationService instance;
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
     * @param job The job to subscribe to.
     * @return String representing websocket topic.
     */
    public static String getJobTopic(Job job) {
        return String.format("/app/jobs/%s", job.getId());
    }

    public static NotificationService getInstance() {
        return instance;
    }

    @PostConstruct
    public void init() {
        instance = this;
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

    /**
     * Sends job to topic subscribers.
     *
     * @param job The job to broadcast.
     */
    public void broadUpdateJobMessage(Job job) {
        System.out.println("SENDING JOB MESSAGE:");
        String versionTopicDestination = getJobTopic(job);
        messagingTemplate.convertAndSend(versionTopicDestination, job);
    }
}
