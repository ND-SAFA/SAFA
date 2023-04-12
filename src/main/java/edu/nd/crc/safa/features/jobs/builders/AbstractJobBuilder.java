package edu.nd.crc.safa.features.jobs.builders;

import java.io.IOException;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;

/**
 * Defines a job performing some actions on some identified entity.
 */
public abstract class AbstractJobBuilder {
    /**
     * List of services.
     */
    protected ServiceProvider serviceProvider;
    /**
     * The database entity for this job.
     */
    protected JobDbEntity jobDbEntity;

    protected SafaUser user;

    protected AbstractJobBuilder(ServiceProvider serviceProvider) {
        this(serviceProvider, null);
    }

    protected AbstractJobBuilder(ServiceProvider serviceProvider, SafaUser user) {
        this.serviceProvider = serviceProvider;
        this.user = user;
    }

    public JobAppEntity perform() throws Exception {
        // Step 1 - Create database entity
        JobService jobService = this.serviceProvider.getJobService();

        if (this.user == null) {
            this.jobDbEntity = jobService.createNewJob(this.getJobType(), this.getJobName());
        } else {
            this.jobDbEntity = jobService.createNewJobForUser(this.getJobType(), this.getJobName(), this.user);
        }

        // Step 3 - Construct job definition
        AbstractJob abstractJob = this.constructJobForWork();

        // Step 4 - Start job
        this.serviceProvider
            .getJobService()
            .executeJob(this.serviceProvider, abstractJob);

        // Step 5 - Return job
        return JobAppEntity.createFromJob(this.jobDbEntity);
    }

    /**
     * Creates job definition for change.
     */
    protected abstract AbstractJob constructJobForWork() throws IOException;

    /**
     * Returns the name of the job.
     *
     * @return The name of the job.
     */
    protected abstract String getJobName();

    /**
     * @return The type of job used to identify operation being performed.return
     */
    protected abstract Class<? extends AbstractJob> getJobType();

    @AllArgsConstructor
    protected static class JobDefinition {
        JobDbEntity jobDbEntity;
        AbstractJob abstractJob;
    }
}
