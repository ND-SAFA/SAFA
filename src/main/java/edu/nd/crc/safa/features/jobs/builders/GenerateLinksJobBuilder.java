package edu.nd.crc.safa.features.jobs.builders;

import java.io.IOException;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.GenerateLinksJob;
import edu.nd.crc.safa.features.models.tgen.entities.TraceGenerationRequest;

/**
 * Creates a job for generating trace links.
 */
public class GenerateLinksJobBuilder extends AbstractJobBuilder<TraceGenerationRequest> {
    TraceGenerationRequest request;

    public GenerateLinksJobBuilder(ServiceProvider serviceProvider,
                                   TraceGenerationRequest request) {
        super(serviceProvider);
        this.request = request;
    }

    @Override
    protected TraceGenerationRequest constructIdentifier() {
        return request;
    }

    @Override
    AbstractJob constructJobForWork() throws IOException {
        ProjectCommit projectCommit = new ProjectCommit(this.request.getProjectVersion(), false);
        return new GenerateLinksJob(this.jobDbEntity, this.serviceProvider, projectCommit, this.request);
    }

    @Override
    String getJobName() {
        return GenerateLinksJob.getJobName(request);
    }

    @Override
    Class<? extends AbstractJob> getJobType() {
        return GenerateLinksJob.class;
    }
}
