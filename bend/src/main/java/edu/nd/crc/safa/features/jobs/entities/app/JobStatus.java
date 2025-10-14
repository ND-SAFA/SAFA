package edu.nd.crc.safa.features.jobs.entities.app;

/**
 * Enumerates the states a job can be found in.
 */
public enum JobStatus {
    IN_PROGRESS,
    COMPLETED,
    CANCELLED,
    FAILED;

    @Override
    public String toString() {
        return this.name();
    }
}
