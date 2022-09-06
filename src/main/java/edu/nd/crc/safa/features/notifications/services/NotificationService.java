package edu.nd.crc.safa.features.notifications.services;

import java.util.UUID;

import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;

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
     * Returns topic for given entity id.
     *
     * @param id ID of the entity to subs
     * @return {@link String} representing topic destination
     */
    public static String getTopic(UUID id) {
        return String.format("/topic/%s", id);
    }

    /**
     * Broadcasts change in given builder.
     *
     * @param builder Builder for {@link edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage} to send.
     */
    public void broadcastChange(EntityChangeBuilder builder) {
        SafaUser safaUser = this.safaUserService.getCurrentUser();
        EntityChangeMessage message = builder.get(safaUser.getEmail());
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
    private void broadcastObject(String topic, Object payload) {
        messagingTemplate.convertAndSend(topic, payload);
    }
}
