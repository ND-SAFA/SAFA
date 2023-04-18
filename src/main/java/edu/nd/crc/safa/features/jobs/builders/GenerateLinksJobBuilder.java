package edu.nd.crc.safa.features.jobs.builders;

import java.io.IOException;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.GenerateLinksJob;
import edu.nd.crc.safa.features.models.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

/**
 * Creates a job for generating trace links.
 */
public class GenerateLinksJobBuilder extends AbstractJobBuilder {
    TraceGenerationRequest request;

    private SafaUser user;

    public GenerateLinksJobBuilder(ServiceProvider serviceProvider,
                                   TraceGenerationRequest request,
                                   SafaUser user) {
        super(serviceProvider);
        this.request = request;
        this.user = user;
    }

    @Override
    protected AbstractJob constructJobForWork() throws IOException {
        ProjectCommit projectCommit = new ProjectCommit(this.request.getProjectVersion(), false);
        return new GenerateLinksJob(this.jobDbEntity, this.serviceProvider, projectCommit, this.request, this.user);
    }

    @Override
    protected String getJobName() {
        return GenerateLinksJob.getJobName(request);
    }

    @Override
    protected Class<? extends AbstractJob> getJobType() {
        return GenerateLinksJob.class;
    }
}
