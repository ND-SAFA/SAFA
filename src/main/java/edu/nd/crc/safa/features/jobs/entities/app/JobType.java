package edu.nd.crc.safa.features.jobs.entities.app;

import edu.nd.crc.safa.features.jobs.entities.jobs.CreateProjectViaJiraJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.CreateProjectViaJsonJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.FlatFileProjectCreationJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.GenerateLinksJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.GithubProjectCreationJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.GithubProjectImportJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.GithubProjectUpdateJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.JiraProjectImportJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.JiraProjectUpdateJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.TrainModelJob;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * Enumerates all the possible types of jobs.
 */
@Getter
@AllArgsConstructor
public enum JobType {
    PROJECT_CREATION_VIA_FLAT_FILE(FlatFileProjectCreationJob.class),
    PROJECT_CREATION_VIA_JIRA(CreateProjectViaJiraJob.class),
    PROJECT_CREATION_VIA_JSON(CreateProjectViaJsonJob.class),
    PROJECT_CREATION_VIA_GITHUB(GithubProjectCreationJob.class),
    PROJECT_UPDATE_VIA_JIRA(JiraProjectUpdateJob.class),
    PROJECT_UPDATE_VIA_GITHUB(GithubProjectUpdateJob.class),
    IMPORT_VIA_JIRA(JiraProjectImportJob.class),
    IMPORT_VIA_GITHUB(GithubProjectImportJob.class),
    TRAIN_MODEL(TrainModelJob.class),
    GENERATE_LINKS(GenerateLinksJob.class);

    private final Class<? extends AbstractJob> jobClass;

    @Override
    public String toString() {
        return this.name();
    }
}
