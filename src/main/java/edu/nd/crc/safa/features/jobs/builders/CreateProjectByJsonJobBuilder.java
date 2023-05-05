package edu.nd.crc.safa.features.jobs.builders;

import java.util.List;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.CreateProjectViaJsonJob;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.tgen.entities.TracingRequest;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

/**
 * Builds job for creating a project via JSON.
 */
public class CreateProjectByJsonJobBuilder extends AbstractJobBuilder {

    private final SafaUser projectOwner;
    /**
     * The project requested to create.
     */
    ProjectAppEntity projectAppEntity;
    /**
     * Requests to generate trace links.
     */
    TraceGenerationRequest traceGenerationRequest;

    public CreateProjectByJsonJobBuilder(ServiceProvider serviceProvider,
                                         ProjectAppEntity projectAppEntity,
                                         List<TracingRequest> tracingRequests,
                                         SafaUser projectOwner) {
        super(serviceProvider);
        this.projectAppEntity = projectAppEntity;
        this.traceGenerationRequest = new TraceGenerationRequest();
        this.traceGenerationRequest.setRequests(tracingRequests);
        this.projectOwner = projectOwner;
    }

    @Override
    protected AbstractJob constructJobForWork() {
        // Step - Create job
        return new CreateProjectViaJsonJob(
            this.jobDbEntity,
            this.projectAppEntity,
            this.serviceProvider,
            this.traceGenerationRequest,
            this.projectOwner
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
