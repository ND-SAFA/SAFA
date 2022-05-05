package edu.nd.crc.safa.server.entities.db;

import java.sql.Timestamp;
import java.util.UUID;
import javax.annotation.Nullable;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.server.entities.api.JobType;
import edu.nd.crc.safa.server.entities.app.JobStatus;

import org.hibernate.annotations.Type;

/**
 * Responsible for storing the information needed to create jobs.
 */
@Entity
@Table(name = "job")
public class Job {

    /**
     * The name of job (e.g. project creation).
     */
    @NotNull
    @Column(name = "job_type", nullable = false)
    protected JobType jobType;
    /**
     * The unique identifier for job.
     */
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "id")
    @NotNull
    UUID id;
    /**
     * The status of the job.
     */
    @NotNull
    @Column(name = "status", nullable = false)
    JobStatus status;
    /**
     * The datetime that a job was started at.
     */
    @NotNull
    @Column(name = "started_at", nullable = false)
    Timestamp startedAt;
    /**
     * The datetime that the last update was received.
     */
    @NotNull
    @Column(name = "last_updated_at", nullable = false)
    Timestamp lastUpdatedAt;
    /**
     * The datetime that the job was completed at, null otherwise.
     */
    @Nullable
    @Column(name = "completed_at")
    Timestamp completedAt;
    /**
     * The current integer percentage of the job that has been completed.
     */
    @NotNull
    @Column(name = "current_progress", nullable = false)
    int currentProgress;
    /**
     * The current step the job is on.
     */
    @NotNull
    @Column(name = "current_step", nullable = false)
    int currentStep;

    public Job() {
    }

    public Job(JobType jobType,
               JobStatus status,
               Timestamp startedAt,
               Timestamp lastUpdatedAt,
               @Nullable Timestamp completedAt,
               int currentProgress,
               int currentStep) {
        this.jobType = jobType;
        this.status = status;
        this.startedAt = startedAt;
        this.lastUpdatedAt = lastUpdatedAt;
        this.completedAt = completedAt;
        this.currentProgress = currentProgress;
        this.currentStep = currentStep;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public JobType getJobType() {
        return jobType;
    }

    public void setJobType(JobType jobType) {
        this.jobType = jobType;
    }

    public JobStatus getStatus() {
        return status;
    }

    public void setStatus(JobStatus status) {
        this.status = status;
    }

    public Timestamp getStartedAt() {
        return startedAt;
    }

    public void setStartedAt(Timestamp startedAt) {
        this.startedAt = startedAt;
    }

    public Timestamp getLastUpdatedAt() {
        return lastUpdatedAt;
    }

    public void setLastUpdatedAt(Timestamp lastUpdatedAt) {
        this.lastUpdatedAt = lastUpdatedAt;
    }

    @Nullable
    public Timestamp getCompletedAt() {
        return completedAt;
    }

    public void setCompletedAt(@Nullable Timestamp completedAt) {
        this.completedAt = completedAt;
    }

    public int getCurrentProgress() {
        return currentProgress;
    }

    public void setCurrentProgress(int currentProgress) {
        this.currentProgress = currentProgress;
    }

    public int getCurrentStep() {
        return currentStep;
    }

    public void setCurrentStep(int currentStep) {
        this.currentStep = currentStep;
    }

    public void incrementStep() {
        this.currentStep++;
    }
}
