package edu.nd.crc.safa.test.features.jobs.base;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.UUID;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.JobStatus;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;

public interface JobTestService {
    static JobDbEntity verifyJobWasCompleted(ServiceProvider serviceProvider,
                                             UUID jobId,
                                             int nSteps) {
        JobDbEntity jobDbEntity = serviceProvider.getJobService().getJobById(jobId);
        assertThat(jobDbEntity.getCurrentProgress()).isEqualTo(100);
        assertThat(jobDbEntity.getStatus()).isEqualTo(JobStatus.COMPLETED);
        assertThat(jobDbEntity.getCurrentStep()).isEqualTo(nSteps - 1);

        // Step - Assert that start is before completed.
        assert jobDbEntity.getCompletedAt() != null;
        int comparison = jobDbEntity.getCompletedAt().compareTo(jobDbEntity.getStartedAt());
        assertThat(comparison).isEqualTo(1);

        // Step - Assert that lastUpdatedBy is after start.
        comparison = jobDbEntity.getLastUpdatedAt().compareTo(jobDbEntity.getStartedAt());
        assertThat(comparison).isEqualTo(1);

        return jobDbEntity;
    }
}
