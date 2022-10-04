package edu.nd.crc.safa.features.jobs.builders;

import java.io.IOException;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobType;
import edu.nd.crc.safa.features.jobs.entities.jobs.TrainModelJob;
import edu.nd.crc.safa.features.models.entities.api.TrainingRequest;
import edu.nd.crc.safa.features.projects.entities.db.Project;

/**
 * Responsible for building a job for training a model.
 */
public class TrainModelJobBuilder extends AbstractJobBuilder<TrainingRequest> {
    private final Project project;
    private final TrainingRequest trainingRequest;

    public TrainModelJobBuilder(ServiceProvider serviceProvider,
                                TrainingRequest trainingRequest,
                                Project project) {
        super(serviceProvider);
        this.project = project;
        this.trainingRequest = trainingRequest;
    }

    @Override
    protected TrainingRequest constructIdentifier() {
        return this.trainingRequest;
    }

    @Override
    AbstractJob constructJobForWork() throws IOException {
        return new TrainModelJob(
            jobDbEntity,
            serviceProvider,
            this.project,
            this.trainingRequest
        );
    }

    @Override
    String getJobName() {
        String modelName = this.identifier.getRequests().get(0).getModel().getName();
        return String.format("Training model: [%s].", modelName);
    }

    @Override
    JobType getJobType() {
        return JobType.TRAIN_MODEL;
    }
}
