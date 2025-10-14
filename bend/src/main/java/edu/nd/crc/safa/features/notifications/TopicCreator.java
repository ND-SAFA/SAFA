package edu.nd.crc.safa.features.notifications;

import java.util.UUID;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class TopicCreator {
    public static String getProjectTopic(UUID id) {
        return Topic.PROJECT.getFormattedPath() + "/" + id;
    }

    /**
     * Creates topic for version.
     *
     * @param id ID of project version.
     * @return Destination for all updates to project version.
     */
    public static String getVersionTopic(UUID id) {
        return Topic.VERSION.getFormattedPath() + "/" + id;
    }

    /**
     * Creates topic for job.
     *
     * @param jobId ID of job.
     * @return Destination for all job updates.
     */
    public static String getJobTopic(UUID jobId) {
        return Topic.JOBS.getFormattedPath() + "/" + jobId;
    }

    /**
     * Creates topic for user.
     *
     * @param userId ID of user.
     * @return Destination for direct messages to users.
     */
    public static String getUserTopic(UUID userId) {
        return Topic.USERS.getFormattedPath() + "/" + userId + "/updates";
    }
}
