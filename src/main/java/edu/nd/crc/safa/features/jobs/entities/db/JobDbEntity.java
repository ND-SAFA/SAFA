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
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;
import org.hibernate.annotations.UpdateTimestamp;

/**
 * Responsible for storing the information needed to create jobs.
 */
@Entity
@Table(name = "job")
@Getter
@Setter
@NoArgsConstructor
public class JobDbEntity {
    /**
     * The name of job (e.g. project creation).
     */
    @NotNull
    @Column(name = "job_type", nullable = false)
    protected Class<? extends AbstractJob> jobType;
    /**
     * The name of the job used for as a human readable description / id.
     */
    @Lob
    @Column(name = "name", nullable = false, columnDefinition = "mediumtext")
    String name;
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
    @UpdateTimestamp
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

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JsonIgnore
    @JoinColumn(
        name = "user_id",
        nullable = false)
    SafaUser user;

    /**
     * The id of the entity that been created or modified with this job.
     */
    @Column(name = "completed_entity_id")
    @Type(type = "uuid-char")
    UUID completedEntityId;

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
}
