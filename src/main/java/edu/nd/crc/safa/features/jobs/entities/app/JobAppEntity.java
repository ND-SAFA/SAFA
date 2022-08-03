package edu.nd.crc.safa.features.jobs.entities.app;

import java.lang.reflect.Field;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;

/**
 * Represents a job's information for presenting its current progress.
 */
public class JobAppEntity extends JobDbEntity {

    /**
     * The list of steps that must be performed for this job.
     */
    String[] steps;

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
            throw new SafaError("Illegally accessed field while creating job app entity.");
        }
    }

    public String[] getSteps() {
        return steps;
    }

    public void setSteps(String[] steps) {
        this.steps = steps;
    }
}
