package edu.nd.crc.safa.server.entities.app;

import java.lang.reflect.Field;

import edu.nd.crc.safa.server.entities.db.JobDbEntity;

/**
 * Represents a job's information for presenting its current progress.
 */
public class JobDbEntityAppEntity extends JobDbEntity {

    /**
     * The list of steps that must be performed for this job.
     */
    String[] steps;

    public JobDbEntityAppEntity() {
        super();
    }

    public static JobDbEntityAppEntity createFromJob(JobDbEntity jobDbEntity) throws IllegalAccessException {
        JobDbEntityAppEntity jobAppEntity = new JobDbEntityAppEntity();
        for (Field f : jobDbEntity.getClass().getDeclaredFields()) {
            f.setAccessible(true);
            f.set(jobAppEntity, f.get(jobDbEntity));
        }
        jobAppEntity.steps = JobSteps.getJobSteps(jobAppEntity.jobType);
        return jobAppEntity;
    }

    public String[] getSteps() {
        return steps;
    }

    public void setSteps(String[] steps) {
        this.steps = steps;
    }
}
