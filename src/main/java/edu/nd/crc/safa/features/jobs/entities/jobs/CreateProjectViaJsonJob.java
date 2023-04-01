package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.util.List;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.models.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

public class CreateProjectViaJsonJob extends CommitJob {
    private final ProjectAppEntity projectAppEntity;
    /**
     * Trace links to generate.
     */
    TraceGenerationRequest traceGenerationRequest;

    private final SafaUser projectOwner;

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
        createProject(projectOwner, projectAppEntity.getName(), projectAppEntity.getDescription());
    }

    @IJobStep(value = "Generating Trace Links", position = 2)
    public void generateLinks(JobLogger logger) {
        TraceGenerationRequest request = this.traceGenerationRequest;
        ProjectAppEntity projectAppEntity = new ProjectAppEntity(getProjectCommit());

        List<TraceAppEntity> generatedTraces = this.serviceProvider
            .getTraceGenerationService()
            .generateTraceLinks(request, projectAppEntity);
        getProjectCommit().addTraces(ModificationType.ADDED, generatedTraces);
        logger.log("Links generated: %s", generatedTraces.size());
    }
}
