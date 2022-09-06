package edu.nd.crc.safa.features.jobs.entities;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

/**
 * Defines a step's position and name in a job.
 */
@Retention(RetentionPolicy.RUNTIME)
public @interface IJobStep {
    /**
     * @return {@link Integer} Position at which the step will be performed.
     */
    int position();

    /**
     * @return {@link String} The name of the job.
     */
    String name();
}
