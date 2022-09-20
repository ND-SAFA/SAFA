package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.tgen.entities.BaseGenerationModels;
import edu.nd.crc.safa.features.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

public class CreateProjectViaJsonJob extends CommitJob {
    /**
     * Trace links to generate.
     */
    List<TraceGenerationRequest> generationRequests;

    public CreateProjectViaJsonJob(JobDbEntity jobDbEntity,
                                   ServiceProvider serviceProvider,
                                   ProjectCommit projectCommit,
                                   List<TraceGenerationRequest> generationRequests) {
        super(jobDbEntity, serviceProvider, projectCommit);
        this.generationRequests = generationRequests;
        this.projectCommit = projectCommit;
    }

    @IJobStep(value = "Generating Trace Links", position = 1)
    public void generateLinks() {
        for (TraceGenerationRequest request : this.generationRequests) {
            if (request.size() == 0) {
                return;
            }
            List<ArtifactAppEntity> sourceArtifacts = request.getSourceArtifacts();
            List<ArtifactAppEntity> targetArtifacts = request.getTargetArtifacts();
            BaseGenerationModels method = request.getMethod();

            List<TraceAppEntity> generatedTraces = this.serviceProvider
                .getTraceGenerationService()
                .generateLinksWithMethod(sourceArtifacts, targetArtifacts, method);
            this.projectCommit.addTraces(ModificationType.ADDED, generatedTraces);
        }
    }
}
