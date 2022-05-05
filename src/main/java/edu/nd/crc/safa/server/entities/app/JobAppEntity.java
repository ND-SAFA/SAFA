package edu.nd.crc.safa.server.entities.app;

import java.lang.reflect.Field;

import edu.nd.crc.safa.server.entities.db.Job;

/**
 * Represents a job's information for presenting its current progress.
 */
public class JobAppEntity extends Job {

    /**
     * The list of steps that must be performed for this job.
     */
    String[] steps;

    public JobAppEntity() {
        super();
    }

    public static JobAppEntity createFromJob(Job job) throws IllegalAccessException {
        JobAppEntity jobAppEntity = new JobAppEntity();
        for (Field f : job.getClass().getDeclaredFields()) {
            f.setAccessible(true);
            f.set(jobAppEntity, f.get(job));
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
