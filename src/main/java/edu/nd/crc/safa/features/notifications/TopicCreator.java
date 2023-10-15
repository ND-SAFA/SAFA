package edu.nd.crc.safa.features.notifications;

import java.util.UUID;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class TopicCreator {
    public static String getProjectTopic(UUID id) {
        return String.format("/topic/project/%s", id);
    }

    public static String getVersionTopic(UUID id) {
        return String.format("/topic/version/%s", id);
    }

    public static String getJobTopic(UUID jobId) {
        return String.format("/topic/jobs/%s", jobId);
    }
}
