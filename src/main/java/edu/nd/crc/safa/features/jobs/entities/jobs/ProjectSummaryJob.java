package edu.nd.crc.safa.features.jobs.entities.jobs;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class ProjectSummaryJob extends CommitJob {
    public ProjectSummaryJob(SafaUser user,
                             ServiceProvider serviceProvider,
                             JobDbEntity jobDbEntity,
                             ProjectVersion projectVersion) {
        super(user, jobDbEntity, serviceProvider, new ProjectCommitDefinition(), false);
        this.getProjectCommitDefinition().setCommitVersion(projectVersion);
    }

    @IJobStep(value = "Create Project Summary", position = 1)
    public void summarizeProjectEntities() {
        ProjectVersion projectVersion = this.getProjectVersion();
        ProjectAppEntity projectAppEntity =
            getServiceProvider().getProjectRetrievalService().getProjectAppEntity(projectVersion);
        this.getServiceProvider().getProjectSummaryService().summaryProjectAppEntity(
            getUser(),
            projectAppEntity,
            getDbLogger(),
            true
        );
    }
}
