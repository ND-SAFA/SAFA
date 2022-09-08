package edu.nd.crc.safa.features.jobs.builders;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobType;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

/**
 * Builds job for creating a project via JSON.
 */
public class CreateProjectByJsonJobBuilder extends AbstractJobBuilder<ProjectVersion> {

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
    AbstractJob constructJobForWork() {
        // Step - Create initial commit
        projectAppEntity.setProjectVersion(this.identifier);
        ProjectCommit projectCommit = new ProjectCommit(projectAppEntity);

        // Step - Create job
        return new CommitJob(
            this.jobDbEntity,
            serviceProvider,
            projectCommit
        );
    }

    @Override
    String getJobName() {
        String projectName = this.identifier.getProject().getName();
        return String.format("Creating project %s.", projectName);
    }

    @Override
    JobType getJobType() {
        return JobType.PROJECT_CREATION;
    }
}
