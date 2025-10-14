package edu.nd.crc.safa.features.generation.common;

import java.util.List;

/**
 * Represents the status of a celery task.
 */
public enum CeleryStatus {
    NOT_STARTED,
    IN_PROGRESS,
    SUCCESS,
    FAILURE,
    REVOKED;

    /**
     * @return Whether the task has failed based on its status.
     */
    public boolean hasFailed() {
        List<CeleryStatus> failedStatus = List.of(FAILURE, REVOKED);
        return failedStatus.contains(this);
    }

    /**
     * @return Whether the task has succeeded based on its status.
     */
    public boolean hasCompleted() {
        return this == SUCCESS;
    }
}
