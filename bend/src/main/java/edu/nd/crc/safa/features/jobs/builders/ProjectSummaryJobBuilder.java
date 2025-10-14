package edu.nd.crc.safa.features.jobs.builders;

import java.io.IOException;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.ProjectSummaryJob;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class ProjectSummaryJobBuilder extends AbstractJobBuilder {
    private final ProjectVersion projectVersion;

    public ProjectSummaryJobBuilder(SafaUser user,
                                    ServiceProvider serviceProvider,
                                    ProjectVersion projectVersion) {
        super(user, serviceProvider);
        this.projectVersion = projectVersion;
    }

    @Override
    protected AbstractJob constructJobForWork() throws IOException {
        return new ProjectSummaryJob(getUser(), this.getServiceProvider(), this.getJobDbEntity(), this.projectVersion);
    }

    @Override
    protected String getJobName() {
        return "Project Summary";
    }

    @Override
    protected Class<? extends AbstractJob> getJobType() {
        return ProjectSummaryJob.class;
    }
}
