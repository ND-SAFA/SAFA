package edu.nd.crc.safa.features.jobs.entities;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;

/**
 * <p>Defines a step's position and name in a job.</p>
 *
 * <p>The job name is purely cosmetic, and will be displayed to the user when the job is executed.</p>
 *
 * <p>The step position is used to determine the order that job steps will be executed in. These values
 * can be positive or negative, with negative values indicating that the step should be added at
 * the end of the list of steps. This is useful when defining a superclass that has a step that
 * should run after all steps in any subclass, regardless of how many there are.</p>
 *
 * <p>Methods annotated with this annotation should return {@code void}, and accept either no parameters
 * or have a single {@link JobLogger} to be able to send relevant logs to the user. These methods
 * should return normally on success or throw an exception on failure.</p>
 *
 * <p>An example of a class with these annotations:<br>
 * <pre>{@code
 * class FooJob extends AbstractJob {
 *     // Will be run first
 *     @IJobStep(value = "Run foo method", position = 1)
 *     public void foo() {}
 *
 *     // Will be run second
 *     @IJobStep(value = "Run bar method", position = 2)
 *     public void bar() {}
 *
 *     // Will be run second to last (i.e. third)
 *     @IJobStep(value = "Run baz method", position = -2)
 *     public void baz() {}
 *
 *     // Will be run last (i.e. fourth)
 *     @IJobStep(value = "Run end method", position = -1)
 *     public void end() {}
 * }
 * }</pre>
 * </p>
 *
 * <p>Note that no checks are made to ensure positions are unique and that they do not exceed the
 * bounds of the list of steps (e.g. having a step with {@code position = 20} when there are only
 * 5 steps). The programmer should ensure that positive steps are consecutive starting at 1 and negative
 * steps are consecutive ending at -1 ({@link AbstractJob} already defines a step at position -1,
 * so really negative steps should end at -2).</p>
 */
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface IJobStep {
    /**
     * @return {@link Integer} Position at which the step will be performed.
     */
    int position();

    /**
     * @return {@link String} The name of the job.
     */
    String value();
}
