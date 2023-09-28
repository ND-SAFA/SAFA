package edu.nd.crc.safa.features.jobs.entities.app;

import java.sql.Timestamp;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;

import lombok.Data;

/**
 * Represents a job's information for presenting its current progress.
 */
@Data
public class JobAppEntity {
    private String name;
    private UUID id;
    private JobStatus status;
    private Timestamp startedAt;
    private Timestamp lastUpdatedAt;
    private Timestamp completedAt;
    private int currentProgress;
    private int currentStep;
    private UUID projectId;
    private UUID completedEntityId;
    private UUID taskId;
    private List<String> steps;

    public JobAppEntity(JobDbEntity jobDbEntity) {
        this.name = jobDbEntity.getName();
        this.id = jobDbEntity.getId();
        this.status = jobDbEntity.getStatus();
        this.startedAt = jobDbEntity.getStartedAt();
        this.lastUpdatedAt = jobDbEntity.getLastUpdatedAt();
        this.completedAt = jobDbEntity.getCompletedAt();
        this.currentProgress = jobDbEntity.getCurrentProgress();
        this.currentStep = jobDbEntity.getCurrentStep();
        this.projectId = jobDbEntity.getProjectId();
        this.completedEntityId = jobDbEntity.getCompletedEntityId();
        this.taskId = jobDbEntity.getTaskId();
    }

    public JobAppEntity() {
        super();
    }

    public static JobAppEntity createFromJob(JobDbEntity jobDbEntity) {
        JobAppEntity jobAppEntity = new JobAppEntity(jobDbEntity);
        jobAppEntity.steps = JobSteps.getJobSteps(jobDbEntity.getJobType());
        return jobAppEntity;
    }
}
