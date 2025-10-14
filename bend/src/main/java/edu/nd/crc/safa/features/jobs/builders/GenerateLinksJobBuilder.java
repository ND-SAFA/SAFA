package edu.nd.crc.safa.features.jobs.builders;

import java.io.IOException;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.generation.tgen.entities.TGenRequestAppEntity;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.GenerateLinksJob;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

/**
 * Creates a job for generating trace links.
 */
public class GenerateLinksJobBuilder extends AbstractJobBuilder {
    private final TGenRequestAppEntity request;

    public GenerateLinksJobBuilder(SafaUser user,
                                   ServiceProvider serviceProvider,
                                   TGenRequestAppEntity request) {
        super(user, serviceProvider);
        this.request = request;
        this.setUser(user);
    }

    @Override
    protected AbstractJob constructJobForWork() throws IOException {
        ProjectCommitDefinition projectCommitDefinition =
            new ProjectCommitDefinition(
                getUser(),
                this.request.getProjectVersion(),
                false
            );
        return new GenerateLinksJob(getUser(),
            this.getJobDbEntity(),
            this.getServiceProvider(),
            projectCommitDefinition,
            this.request);
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
