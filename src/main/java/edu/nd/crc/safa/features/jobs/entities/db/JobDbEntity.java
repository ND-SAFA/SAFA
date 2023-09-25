package edu.nd.crc.safa.features.jobs.entities.db;

import static java.lang.Math.round;

import java.sql.Timestamp;
import java.util.UUID;
import javax.annotation.Nullable;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.Lob;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobStatus;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;
import org.hibernate.annotations.UpdateTimestamp;

/**
 * Responsible for storing the information needed to create jobs.
 */
@Entity
@Table(name = "job")
@Data
@NoArgsConstructor
public class JobDbEntity {

    /**
     * The name of job (e.g. project creation).
     */
    @JsonIgnore
    @NotNull
    @Column(name = "job_type", nullable = false)
    private Class<? extends AbstractJob> jobType;
    /**
     * The name of the job used for as a human readable description / id.
     */
    @Lob
    @Column(name = "name", nullable = false, columnDefinition = "mediumtext")
    private String name;
    /**
     * The unique identifier for job.
     */
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "id")
    @NotNull
    private UUID id;
    /**
     * The status of the job.
     */
    @NotNull
    @Column(name = "status", nullable = false)
    private JobStatus status;
    /**
     * The datetime that a job was started at.
     */
    @NotNull
    @Column(name = "started_at", nullable = false)
    private Timestamp startedAt;
    /**
     * The datetime that the last update was received.
     */
    @NotNull
    @Column(name = "last_updated_at", nullable = false)
    @UpdateTimestamp
    private Timestamp lastUpdatedAt;
    /**
     * The datetime that the job was completed at, null otherwise.
     */
    @Nullable
    @Column(name = "completed_at")
    private Timestamp completedAt;
    /**
     * The current integer percentage of the job that has been completed.
     */
    @NotNull
    @Column(name = "current_progress", nullable = false)
    private int currentProgress;
    /**
     * The current step the job is on.
     */
    @NotNull
    @Column(name = "current_step", nullable = false)
    private int currentStep;
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JsonIgnore
    @JoinColumn(
        name = "user_id",
        nullable = false)
    private SafaUser user;
    @ManyToOne
    @JsonIgnore
    @JoinColumn(name = "project_id")
    private Project project;
    @Column(name = "completed_entity_id")
    @Type(type = "uuid-char")
    private UUID completedEntityId;

    @Column(name = "task_id", nullable = true)
    private UUID taskId;

    public JobDbEntity(SafaUser user,
                       String name,
                       Class<? extends AbstractJob> jobType,
                       JobStatus status,
                       Timestamp startedAt,
                       Timestamp lastUpdatedAt,
                       @Nullable Timestamp completedAt,
                       int currentProgress,
                       int currentStep) {
        this.user = user;
        this.name = name;
        this.jobType = jobType;
        this.status = status;
        this.startedAt = startedAt;
        this.lastUpdatedAt = lastUpdatedAt;
        this.completedAt = completedAt;
        this.currentProgress = currentProgress;
        this.currentStep = currentStep;
        this.completedEntityId = null;
    }

    public void incrementStep() {
        this.currentStep++;
    }

    public void incrementProgress(int nSteps) {
        float percentComplete = 100 * (this.currentStep / (float) nSteps);
        this.setCurrentProgress(round(percentComplete));
    }

    public UUID getProjectId() {
        return this.project == null ? null : this.getProject().getProjectId();
    }
}
