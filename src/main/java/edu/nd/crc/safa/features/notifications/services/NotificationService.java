package edu.nd.crc.safa.features.notifications.services;

import java.util.UUID;

import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;

import lombok.AllArgsConstructor;
import org.springframework.context.annotation.Scope;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;

/**
 * Responsible for sending notifications to subscribers of certain topics.
 */
@AllArgsConstructor
@Service
@Scope("singleton")
public class NotificationService {

    private final SimpMessagingTemplate messagingTemplate;
    private final SafaUserService safaUserService;
    private final ProjectRepository projectRepository;

    /**
     * Returns topic for given entity id.
     *
     * @param id ID of the entity to subs
     * @return {@link String} representing topic destination
     */
    public static String getTopic(UUID id) {
        return String.format("/topic/%s", id);
    }

    public static String getProjectTopic(UUID id) {
        return String.format("/topic/project/%s", id);
    }

    public static String getVersionTopic(UUID id) {
        return String.format("/topic/version/%s", id);
    }

    public static String getUserTopic(UUID userId) {
        return String.format("/user/%s/updates", userId);
    }

    /**
     * Broadcasts change in given builder.
     *
     * @param builder Builder for {@link edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage} to send.
     */
    public void broadcastChange(EntityChangeBuilder builder) {
        SafaUser safaUser = this.safaUserService.getCurrentUser();
        broadcastChangeToUser(builder, safaUser);
    }

    /**
     * Broadcasts change in given builder to a given user.
     *
     * @param builder Builder for {@link edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage} to send.
     * @param user    User to send message to
     */
    public void broadcastChangeToUser(EntityChangeBuilder builder, SafaUser user) {
        EntityChangeMessage message = builder.get(user.getEmail());
        this.broadcastObject(builder.getTopic(), message);
    }

    public void broadcastJob(JobAppEntity jobAppEntity) {
        this.broadcastObject(jobAppEntity.getTopic(), jobAppEntity);
    }

    /**
     * Sends given object to topic as JSON.
     *
     * @param topic   The destination for the object.
     * @param payload Object to be sent to topic
     */
    public void broadcastObject(String topic, Object payload) {
        messagingTemplate.convertAndSend(topic, payload);
    }
}
