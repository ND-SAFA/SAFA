package edu.nd.crc.safa.features.jobs.entities.app;

/**
 * Enumerates all the possible types of jobs.
 */
public enum JobType {
    PROJECT_CREATION_VIA_FLAT_FILE,
    PROJECT_CREATION_VIA_JIRA,
    PROJECT_CREATION_VIA_JSON,
    PROJECT_CREATION_VIA_GITHUB,
    PROJECT_UPDATE_VIA_JIRA,
    PROJECT_UPDATE_VIA_GITHUB,
    PROJECT_SYNC,
    GENERATE_LAYOUT,
    TRAIN_MODEL,

    GENERATE_LINKS;

    @Override
    public String toString() {
        return this.name();
    }
}
