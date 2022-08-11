package edu.nd.crc.safa.features.jobs.entities.builders;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;

import lombok.AllArgsConstructor;
import org.springframework.batch.core.JobParametersInvalidException;
import org.springframework.batch.core.repository.JobExecutionAlreadyRunningException;
import org.springframework.batch.core.repository.JobInstanceAlreadyCompleteException;
import org.springframework.batch.core.repository.JobRestartException;

/**
 * Defines a job performing some actions on some project version.
 */
public abstract class AbstractJobBuilder<I, W> {
    /**
     * List of services.
     */
    protected ServiceProvider serviceProvider;
    /**
     * Input to job builder.
     */
    I identifier;
    /**
     * Entity affected in job.
     */
    W change;

    protected AbstractJobBuilder(ServiceProvider serviceProvider) {
        this.serviceProvider = serviceProvider;
    }

    public JobAppEntity perform() throws JobInstanceAlreadyCompleteException, JobExecutionAlreadyRunningException, JobParametersInvalidException, JobRestartException {
        // Step 1 - Select project version to change
        this.identifier = this.constructIdentifier();

        // Step - Construct change
        this.change = this.constructJobWork(this.identifier);

        // Step 3 - Construct job definition
        JobDefinition jobDefinition = this.constructJobForWork(this.change);

        // Step 4 - Start job
        JobDbEntity jobDbEntity = jobDefinition.jobDbEntity;
        this.serviceProvider
            .getJobService()
            .executeJob(jobDbEntity,
                serviceProvider,
                jobDefinition.abstractJob);

        // Step 5 - Return job
        return JobAppEntity.createFromJob(jobDbEntity);
    }

    /**
     * Step 1 - Find project version that is getting affected.
     */
    protected abstract I constructIdentifier();

    /**
     * Step 2 - Generate necessary changes to project.
     */
    protected abstract W constructJobWork(I input);

    /**
     * Step 3 - Creates job definition for change.
     */
    abstract JobDefinition constructJobForWork(W change);

    @AllArgsConstructor
    protected static class JobDefinition {
        JobDbEntity jobDbEntity;
        AbstractJob abstractJob;
    }
}
