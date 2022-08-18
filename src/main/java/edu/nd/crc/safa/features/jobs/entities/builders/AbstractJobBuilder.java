package edu.nd.crc.safa.features.jobs.entities.builders;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;

import lombok.AllArgsConstructor;

/**
 * Defines a job performing some actions on some identified entity.
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
     * Work to be done by job.
     */
    W work;

    protected AbstractJobBuilder(ServiceProvider serviceProvider) {
        this.serviceProvider = serviceProvider;
    }

    public JobAppEntity perform() throws Exception {
        // Step 1 - Select project version to change
        this.identifier = this.constructIdentifier();

        // Step - Construct change
        this.work = this.constructJobWork(this.identifier);

        // Step 3 - Construct job definition
        JobDefinition jobDefinition = this.constructJobForWork(this.work);

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
