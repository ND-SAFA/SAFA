package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.util.UUID;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.models.entities.api.TrainingRequest;
import edu.nd.crc.safa.features.models.tgen.entities.TracingRequest;
import edu.nd.crc.safa.features.models.tgen.method.bert.TBert;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class TrainModelJob extends AbstractJob {
    private final Project project;
    private final TrainingRequest trainingRequest;

    public TrainModelJob(JobDbEntity jobDbEntity,
                         ServiceProvider serviceProvider,
                         Project project,
                         TrainingRequest trainingRequest) {
        super(jobDbEntity, serviceProvider);
        this.project = project;
        this.trainingRequest = trainingRequest;
    }

    @IJobStep(value = "Training model", position = 1)
    public void trainModel() {
        ProjectVersion currentVersion = this.serviceProvider.getVersionService().getCurrentVersion(project);
        ProjectAppEntity projectAppEntity =
            this.serviceProvider.getProjectRetrievalService().getProjectAppEntity(currentVersion);

        for (TracingRequest tracingRequest : this.trainingRequest.getRequests()) {
            TBert bertModel = this.serviceProvider.getBertService().getBertModel(
                tracingRequest.getModel().getBaseModel(),
                this.serviceProvider.getSafaRequestBuilder());
            bertModel.trainModel(
                tracingRequest.getModel().getStatePath(),
                tracingRequest,
                projectAppEntity);
        }
    }

    @Override
    protected UUID getCompletedEntityId() {
        return this.trainingRequest.getRequests().get(0).getModel().getId();
    }
}
