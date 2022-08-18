package edu.nd.crc.safa.features.jobs.entities.builders;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobType;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

/**
 * Builds job for creating a project via JSON.
 */
public class CreateProjectByJsonJobBuilder extends AbstractJobBuilder<ProjectVersion, ProjectCommit> {

    /**
     * The project requested to create.
     */
    ProjectAppEntity projectAppEntity;

    public CreateProjectByJsonJobBuilder(ServiceProvider serviceProvider,
                                         ProjectAppEntity projectAppEntity) {
        super(serviceProvider);
        this.projectAppEntity = projectAppEntity;
    }

    @Override
    protected ProjectVersion constructIdentifier() {
        Project project = new Project(
            projectAppEntity.getName(),
            projectAppEntity.getDescription());
        this.serviceProvider
            .getProjectService()
            .saveProjectWithCurrentUserAsOwner(project);
        return this.serviceProvider.getVersionService().createInitialProjectVersion(project);
    }

    @Override
    protected ProjectCommit constructJobWork(ProjectVersion projectVersion) {
        projectAppEntity.setProjectVersion(projectVersion);
        return new ProjectCommit(projectAppEntity);
    }

    @Override
    JobDefinition constructJobForWork(ProjectCommit change) {
        String projectName = this.identifier.getProject().getName();
        String jobName = String.format("Creating project %s.", projectName);
        JobDbEntity jobDbEntity = this.serviceProvider
            .getJobService()
            .createNewJob(JobType.PROJECT_CREATION, jobName);
        CommitJob commitJob = new CommitJob(
            jobDbEntity,
            serviceProvider,
            change
        );
        return new JobDefinition(jobDbEntity, commitJob);
    }
}
