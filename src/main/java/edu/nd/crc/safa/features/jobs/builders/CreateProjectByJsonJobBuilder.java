package edu.nd.crc.safa.features.jobs.builders;

import java.util.List;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.generation.tgen.entities.TGenRequestAppEntity;
import edu.nd.crc.safa.features.generation.tgen.entities.TracingRequest;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.CreateProjectViaJsonJob;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

/**
 * Builds job for creating a project via JSON.
 */
public class CreateProjectByJsonJobBuilder extends AbstractJobBuilder {
    /**
     * The project requested to create.
     */
    private final ProjectAppEntity projectAppEntity;
    /**
     * Requests to generate trace links.
     */
    private final TGenRequestAppEntity TGenRequestAppEntity;

    public CreateProjectByJsonJobBuilder(SafaUser user,
                                         ServiceProvider serviceProvider,
                                         ProjectAppEntity projectAppEntity,
                                         List<TracingRequest> tracingRequests) {
        super(user, serviceProvider);
        this.projectAppEntity = projectAppEntity;
        this.TGenRequestAppEntity = new TGenRequestAppEntity();
        this.TGenRequestAppEntity.setRequests(tracingRequests);
    }

    @Override
    protected AbstractJob constructJobForWork() {
        // Step - Create job
        return new CreateProjectViaJsonJob(
            getUser(),
            this.getJobDbEntity(),
            this.projectAppEntity,
            this.getServiceProvider(),
            this.TGenRequestAppEntity
        );
    }

    @Override
    protected String getJobName() {
        return String.format("Creating project %s.", projectAppEntity.getName());
    }

    @Override
    protected Class<? extends AbstractJob> getJobType() {
        return CreateProjectViaJsonJob.class;
    }
}
