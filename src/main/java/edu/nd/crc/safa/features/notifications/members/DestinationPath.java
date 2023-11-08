package edu.nd.crc.safa.features.notifications.members;

import java.util.UUID;

import lombok.Data;

@Data
public class DestinationPath {
    /**
     * The name of the topic (e.g. /topic/project/abc123 = project)
     */
    private final String topic;
    /**
     * The ID of the topic (e.g. /user/abc123 = abc123).
     */
    private final UUID topicId;

    public DestinationPath(String path) {
        String[] parts = path.split("/");
        if (parts[1].equals("topic")) {
            this.topic = parts[2];
            this.topicId = UUID.fromString(parts[3]);
        } else {
            this.topic = parts[1];
            this.topicId = UUID.fromString(parts[2]);
        }
    }

    public boolean isTopic(String channelName) {
        return this.topic.equals(channelName);
    }
}
