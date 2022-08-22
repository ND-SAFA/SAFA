package edu.nd.crc.safa.features.jobs.entities.app;

import java.lang.reflect.Field;
import java.util.List;

import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * Represents a job's information for presenting its current progress.
 */
@Data
@EqualsAndHashCode(callSuper = true)
public class JobAppEntity extends JobDbEntity {

    /**
     * The list of steps that must be performed for this job.
     */
    List<String> steps;

    public JobAppEntity() {
        super();
    }

    public static JobAppEntity createFromJob(JobDbEntity jobDbEntity) {
        try {
            JobAppEntity jobAppEntity = new JobAppEntity();
            for (Field f : jobDbEntity.getClass().getDeclaredFields()) {
                f.setAccessible(true);
                f.set(jobAppEntity, f.get(jobDbEntity));
            }
            jobAppEntity.steps = JobSteps.getJobSteps(jobAppEntity.jobType);
            return jobAppEntity;
        } catch (IllegalAccessException e) {
            String errorMessage = "Illegally accessed field while creating job app entity. %s";
            throw new SafaError(errorMessage, e.getMessage());
        }
    }
}
