package edu.nd.crc.safa.features.notifications;

import java.util.HashMap;
import java.util.Map;
import java.util.function.Supplier;

import edu.nd.crc.safa.features.notifications.security.JobTopicPermissionCheck;
import edu.nd.crc.safa.features.notifications.security.NoTopicPermissionCheck;
import edu.nd.crc.safa.features.notifications.security.ProjectTopicPermissionCheck;
import edu.nd.crc.safa.features.notifications.security.ProjectVersionTopicPermissionCheck;
import edu.nd.crc.safa.features.notifications.security.TopicPermissionCheckFunction;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
@Getter
public enum Topic {
    USERS("", "users", NoTopicPermissionCheck::new),
    APP("", "app", NoTopicPermissionCheck::new),
    JOBS("topic", "jobs", JobTopicPermissionCheck::new),
    VERSION("topic", "version", ProjectVersionTopicPermissionCheck::new),
    PROJECT("topic", "project", ProjectTopicPermissionCheck::new);

    private final String prefix;
    private final String name;
    private final Supplier<TopicPermissionCheckFunction> permissionFunctionSupplier;

    private static final Map<String, Topic> reverseLookupMap = buildReverseLookup();

    /**
     * Get the full path of this topic in its formatted form
     *
     * @return The formatted path
     */
    public String getFormattedPath() {
        if (this.prefix.isEmpty()) {
            return "/" + this.name;
        } else {
            return "/" + this.prefix + "/" + this.name;
        }
    }

    /**
     * Get a formatted version of the topic's prefix. For topics with no prefix,
     * the name of the topic is treated as the prefix
     *
     * @return The formatted prefix
     */
    public String getFormattedPrefix() {
        if (this.prefix.isEmpty()) {
            return "/" + this.name;
        } else {
            return "/" + this.prefix;
        }
    }

    /**
     * Get a topic definition based on the topic name
     *
     * @param topicName The name of the topic
     * @return The topic with that name, or null if it is not found
     */
    public static Topic fromName(String topicName) {
        return reverseLookupMap.get(topicName);
    }

    /**
     * Builds the reverse lookup map used by {@link #fromName(String)}
     *
     * @return A map from topic name to the topic definition
     */
    private static Map<String, Topic> buildReverseLookup() {
        Map<String, Topic> map = new HashMap<>();
        for (Topic topic : values()) {
            map.put(topic.getName(), topic);
        }
        return map;
    }
}
