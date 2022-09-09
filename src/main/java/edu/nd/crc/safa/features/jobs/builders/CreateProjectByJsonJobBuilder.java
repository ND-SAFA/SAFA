package edu.nd.crc.safa.features.jobs.builders;

import java.util.List;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobType;
import edu.nd.crc.safa.features.jobs.entities.jobs.ProjectProjectViaJsonJob;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

/**
 * Builds job for creating a project via JSON.
 */
public class CreateProjectByJsonJobBuilder extends AbstractJobBuilder<ProjectVersion> {

    /**
     * The project requested to create.
     */
    ProjectAppEntity projectAppEntity;
    /**
     * Requests to generate trace links.
     */
    List<TraceGenerationRequest> traceGenerationRequests;

    public CreateProjectByJsonJobBuilder(ServiceProvider serviceProvider,
                                         ProjectAppEntity projectAppEntity,
                                         List<TraceGenerationRequest> traceGenerationRequests) {
        super(serviceProvider);
        this.projectAppEntity = projectAppEntity;
        this.traceGenerationRequests = traceGenerationRequests;
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
        this.projectAppEntity.setProjectVersion(this.identifier);
        ProjectCommit projectCommit = new ProjectCommit(projectAppEntity);

        // Step - Create job
        return new ProjectProjectViaJsonJob(
            this.jobDbEntity,
            this.serviceProvider,
            projectCommit,
            this.traceGenerationRequests
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
