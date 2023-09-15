package edu.nd.crc.safa.features.jobs.builders;

import java.io.IOException;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.generation.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.GenerateLinksJob;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

/**
 * Creates a job for generating trace links.
 */
public class GenerateLinksJobBuilder extends AbstractJobBuilder {
    private TraceGenerationRequest request;
    private final SafaUser user;

    public GenerateLinksJobBuilder(ServiceProvider serviceProvider,
                                   TraceGenerationRequest request,
                                   SafaUser user) {
        super(serviceProvider);
        this.request = request;
        this.user = user;
    }

    @Override
    protected AbstractJob constructJobForWork() throws IOException {
        ProjectCommitDefinition projectCommitDefinition = new ProjectCommitDefinition(this.request.getProjectVersion(), false);
        return new GenerateLinksJob(this.jobDbEntity, this.serviceProvider, projectCommitDefinition, this.request, this.user);
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
