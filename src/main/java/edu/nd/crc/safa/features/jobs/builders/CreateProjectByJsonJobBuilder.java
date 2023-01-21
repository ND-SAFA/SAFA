package edu.nd.crc.safa.features.jobs.builders;

import java.util.List;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.CreateProjectViaJsonJob;
import edu.nd.crc.safa.features.models.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.models.tgen.entities.TracingRequest;
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
    /**
     * Requests to generate trace links.
     */
    TraceGenerationRequest traceGenerationRequest;

    public CreateProjectByJsonJobBuilder(ServiceProvider serviceProvider,
                                         ProjectAppEntity projectAppEntity,
                                         List<TracingRequest> tracingRequests) {
        super(serviceProvider);
        this.projectAppEntity = projectAppEntity;
        this.traceGenerationRequest = new TraceGenerationRequest();
        this.traceGenerationRequest.setRequests(tracingRequests);
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
        this.traceGenerationRequest.setProjectVersion(this.identifier);
        ProjectCommit projectCommit = new ProjectCommit(projectAppEntity);

        // Step - Create job
        return new CreateProjectViaJsonJob(
            this.jobDbEntity,
            this.serviceProvider,
            projectCommit,
            this.traceGenerationRequest
        );
    }

    @Override
    String getJobName() {
        String projectName = this.identifier.getProject().getName();
        return String.format("Creating project %s.", projectName);
    }

    @Override
    Class<? extends AbstractJob> getJobType() {
        return CreateProjectViaJsonJob.class;
    }
}
