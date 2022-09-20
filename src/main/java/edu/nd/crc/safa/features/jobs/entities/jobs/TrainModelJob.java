package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.util.UUID;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.models.entities.api.TrainingRequest;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.tgen.method.bert.TBert;

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
    public void creatingTrainingData() {
        TBert bertModel = this.serviceProvider.getBertService().getBertModel(
            trainingRequest.getModel().getBaseModel(),
            this.serviceProvider.getSafaRequestBuilder());
        bertModel.trainModel(
            trainingRequest.getModel().getStatePath(project),
            trainingRequest.getSources(),
            trainingRequest.getTargets(),
            trainingRequest.getTraces());
    }

    @Override
    protected UUID getCompletedEntityId() {
        return this.trainingRequest.getModel().getId();
    }
}
