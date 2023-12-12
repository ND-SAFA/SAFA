package edu.nd.crc.safa.features.jobs.builders;

import java.io.IOException;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.generation.hgen.HGenRequest;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.HGenJob;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

/**
 * Creates a job for generating trace links.
 */
public class HGenJobBuilder extends AbstractJobBuilder {
    private final ProjectVersion projectVersion;
    private final HGenRequest request;

    public HGenJobBuilder(ServiceProvider serviceProvider,
                          ProjectVersion projectVersion,
                          HGenRequest request,
                          SafaUser user) {
        super(user, serviceProvider);
        this.projectVersion = projectVersion;
        this.request = request;
    }

    @Override
    protected AbstractJob constructJobForWork() throws IOException {
        ProjectCommitDefinition projectCommitDefinition = new ProjectCommitDefinition(getUser(),
            this.projectVersion,
            false);
        return new HGenJob(getUser(), this.getJobDbEntity(), this.getServiceProvider(), projectCommitDefinition,
            this.request);
    }

    @Override
    protected String getJobName() {
        return HGenJob.getJobName(request);
    }

    @Override
    protected Class<? extends AbstractJob> getJobType() {
        return HGenJob.class;
    }
}
