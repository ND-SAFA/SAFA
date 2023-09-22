package edu.nd.crc.safa.features.jobs.entities.jobs;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class ProjectSummaryJob extends GenerationJob {
    public ProjectSummaryJob(SafaUser user,
                             ServiceProvider serviceProvider,
                             JobDbEntity jobDbEntity,
                             ProjectVersion projectVersion) {
        super(user, jobDbEntity, serviceProvider, new ProjectCommitDefinition());
        this.getProjectCommitDefinition().setCommitVersion(projectVersion);
    }

    @Override
    @IJobStep(value = "Create Project Summary", position = 2)
    public void summarizeProjectEntities() {
        ProjectVersion projectVersion = this.getProjectVersion();
        projectVersion.getProject().setSpecification("");
        super.summarizeProjectEntities();
    }
}
