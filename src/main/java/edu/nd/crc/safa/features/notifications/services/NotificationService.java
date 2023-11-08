package edu.nd.crc.safa.features.notifications.services;

import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.builders.AbstractEntityChangeBuilder;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;

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

    /**
     * Broadcasts change in given builder to a given user.
     *
     * @param builder Builder for {@link edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage} to send.
     */
    public void broadcastChange(AbstractEntityChangeBuilder builder) {
        EntityChangeMessage message = builder.getEntityChangeMessage();
        String topic = message.getTopic();
        this.broadcastObject(topic, message);
    }

    /**
     * Publishes job to its topic.
     *
     * @param jobAppEntity The job to publish.
     */
    public void sendJob(JobAppEntity jobAppEntity) {
        String jobTopic = TopicCreator.getJobTopic(jobAppEntity.getId());
        this.broadcastObject(jobTopic, jobAppEntity);
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
