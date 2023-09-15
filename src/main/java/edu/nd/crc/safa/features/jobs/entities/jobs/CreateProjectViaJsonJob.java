package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.util.List;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.generation.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class CreateProjectViaJsonJob extends CommitJob {
    private final ProjectAppEntity projectAppEntity;
    private final SafaUser projectOwner;
    /**
     * Trace links to generate.
     */
    TraceGenerationRequest traceGenerationRequest;

    public CreateProjectViaJsonJob(JobDbEntity jobDbEntity,
                                   ProjectAppEntity projectAppEntity,
                                   ServiceProvider serviceProvider,
                                   TraceGenerationRequest traceGenerationRequest,
                                   SafaUser projectOwner) {
        super(jobDbEntity, serviceProvider);
        this.traceGenerationRequest = traceGenerationRequest;
        this.projectAppEntity = projectAppEntity;
        this.projectOwner = projectOwner;
    }

    @IJobStep(value = "Creating Project", position = 1)
    public void createProjectStep() {
        ProjectVersion projectVersion =
            createProject(projectOwner, projectAppEntity.getName(), projectAppEntity.getDescription());
        this.projectAppEntity.setProjectVersion(projectVersion);
        this.traceGenerationRequest.setProjectVersion(projectVersion);

        getProjectCommitDefinition().addArtifacts(ModificationType.ADDED, this.projectAppEntity.getArtifacts());
        getProjectCommitDefinition().addTraces(ModificationType.ADDED, this.projectAppEntity.getTraces());
    }

    @IJobStep(value = "Generating Trace Links", position = 2)
    public void generateLinks(JobLogger logger) {
        TraceGenerationRequest request = this.traceGenerationRequest;
        ProjectAppEntity projectAppEntity = new ProjectAppEntity(getProjectCommitDefinition());

        List<TraceAppEntity> generatedTraces = this.serviceProvider
            .getTraceGenerationService()
            .generateTraceLinks(request, projectAppEntity);
        getProjectCommitDefinition().addTraces(ModificationType.ADDED, generatedTraces);
        logger.log("Links generated: %s", generatedTraces.size());
    }
}
