package edu.nd.crc.safa.features.jobs.builders;

import java.io.IOException;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.hgen.HGenRequest;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.GenerateLinksJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.HGenJob;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

/**
 * Creates a job for generating trace links.
 */
public class HGenJobBuilder extends AbstractJobBuilder {
    ProjectVersion projectVersion;
    HGenRequest request;

    public HGenJobBuilder(ServiceProvider serviceProvider,
                          ProjectVersion projectVersion,
                          HGenRequest request,
                          SafaUser user) {
        super(serviceProvider);
        this.projectVersion = projectVersion;
        this.request = request;
        this.user = user;
    }

    @Override
    protected AbstractJob constructJobForWork() throws IOException {
        ProjectCommit projectCommit = new ProjectCommit(this.projectVersion, false);
        return new HGenJob(this.jobDbEntity, this.serviceProvider, projectCommit, this.request);
    }

    @Override
    protected String getJobName() {
        return HGenJob.getJobName(request);
    }

    @Override
    protected Class<? extends AbstractJob> getJobType() {
        return GenerateLinksJob.class;
    }
}
