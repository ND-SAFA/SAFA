package edu.nd.crc.safa.features.notifications;

import java.util.HashMap;
import java.util.Map;
import java.util.function.Supplier;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.notifications.security.JobTopicPermissionCheck;
import edu.nd.crc.safa.features.notifications.security.MembershipEntityTopicPermissionCheck;
import edu.nd.crc.safa.features.notifications.security.NoTopicPermissionCheck;
import edu.nd.crc.safa.features.notifications.security.TopicPermissionCheckFunction;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
@Getter
public enum Topic {
    USERS("", "users", NoTopicPermissionCheck::new),
    APP("", "app", NoTopicPermissionCheck::new),
    JOBS("topic", "jobs", JobTopicPermissionCheck::new),
    VERSION("topic", "version",
            () -> new MembershipEntityTopicPermissionCheck(ProjectPermission.VIEW,
                    id -> sp().getVersionService().getVersionById(id))),
    PROJECT("topic", "project",
            () -> new MembershipEntityTopicPermissionCheck(ProjectPermission.VIEW,
                    id -> sp().getProjectService().getProjectById(id)));

    private final String prefix;
    private final String name;
    private final Supplier<TopicPermissionCheckFunction> permissionFunctionSupplier;

    private static final Map<String, Topic> reverseLookupMap = buildReverseLookup();

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

    /**
     * Shortened name for {@link ServiceProvider#getInstance()}
     *
     * @return The service provider instance
     */
    private static ServiceProvider sp() {
        return ServiceProvider.getInstance();
    }
}
