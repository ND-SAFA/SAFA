package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.util.List;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.models.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

public class CreateProjectViaJsonJob extends CommitJob {
    /**
     * Trace links to generate.
     */
    TraceGenerationRequest traceGenerationRequest;

    public CreateProjectViaJsonJob(JobDbEntity jobDbEntity,
                                   ServiceProvider serviceProvider,
                                   ProjectCommit projectCommit,
                                   TraceGenerationRequest traceGenerationRequest) {
        super(jobDbEntity, serviceProvider, projectCommit);
        this.traceGenerationRequest = traceGenerationRequest;
        this.projectCommit = projectCommit;
    }

    @IJobStep(value = "Generating Trace Links", position = 1)
    public void generateLinks() {
        TraceGenerationRequest request = this.traceGenerationRequest;
        ProjectAppEntity projectAppEntity = new ProjectAppEntity(this.projectCommit);

        List<TraceAppEntity> generatedTraces = this.serviceProvider
            .getTraceGenerationService()
            .generateTraceLinks(request, projectAppEntity);
        this.projectCommit.addTraces(ModificationType.ADDED, generatedTraces);
        System.out.println("Links generated:" + generatedTraces.size());
    }
}
