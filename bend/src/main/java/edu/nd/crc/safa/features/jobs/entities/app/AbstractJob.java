package edu.nd.crc.safa.features.jobs.entities.app;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.UUID;
import java.util.logging.LogManager;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.JobExecutionUtilities;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import com.google.errorprone.annotations.ForOverride;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NonNull;
import lombok.Setter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.batch.core.BatchStatus;
import org.springframework.batch.core.ExitStatus;
import org.springframework.batch.core.Job;
import org.springframework.batch.core.JobExecution;
import org.springframework.batch.core.JobParameters;
import org.springframework.batch.core.JobParametersIncrementer;
import org.springframework.batch.core.JobParametersValidator;
import org.springframework.security.core.Authentication;

/**
 * <p>Responsible for finding methods corresponding to steps in job and running them
 * by providing a default execution method.</p>
 *
 * <p>Subclasses of this class should implement job steps by annotating them with
 * the {@link IJobStep} annotation. See the docs for the annotation for more information
 * on implementing job steps.</p>
 *
 * <p>Callback methods are provided that can be overridden to receive notifications
 * about the progression of the job for the purposes of logging, etc.:<br>
 * {@link #beforeJob()}<br>
 * {@link #afterJob(boolean)}<br>
 * {@link #jobFailed(Exception)}<br>
 * {@link #beforeStep(int, String)}<br>
 * {@link #afterStep(int, String, boolean)}<br>
 * {@link #stepFailed(int, String, Exception)}<br>
 * </p>
 */
@Getter
@Setter
public abstract class AbstractJob implements Job {
    private static final java.util.logging.Logger rootLogger = LogManager.getLogManager().getLogger("");
    /**
     * The job identifying information that is being performed.
     */
    private static final Logger log = LoggerFactory.getLogger(AbstractJob.class);
    @Getter(AccessLevel.PROTECTED)
    private JobDbEntity jobDbEntity;
    /**
     * Service used to send job updates.
     */
    @Getter(AccessLevel.PUBLIC)
    private ServiceProvider serviceProvider;
    private JobService jobService;
    private NotificationService notificationService;
    /**
     * List of step indices to skip.
     */
    private List<Integer> skipSteps = new ArrayList<>();
    /**
     * The authentication to execute job with.
     */
    private Authentication authentication;
    private JobLogger dbLogger;

    protected AbstractJob(JobDbEntity jobDbEntity, ServiceProvider serviceProvider) {
        this.jobDbEntity = jobDbEntity;
        this.serviceProvider = serviceProvider;

        this.jobService = this.serviceProvider.getJobService();
        this.notificationService = this.serviceProvider.getNotificationService();

        this.dbLogger = new JobLogger(serviceProvider.getJobLoggingService(), jobDbEntity, 0);
    }

    /**
     * Execute all job steps.
     *
     * @param execution JobExecution used for restarting jobs (WIP).
     */
    @Override
    public void execute(@NonNull JobExecution execution) {
        List<JobStepImplementation> jobSteps = JobExecutionUtilities.getSteps(this.getClass());
        int nSteps = jobSteps.size();
        boolean success = true;

        try {
            execution.setStatus(BatchStatus.STARTED);
            notifyBeforeJob();
            for (JobStepImplementation stepImplementation : jobSteps) {
                executeJobStep(stepImplementation, nSteps);
            }
        } catch (Exception e) {
            e.printStackTrace();
            success = false;
            notifyJobFailed(e);
        } finally {
            notifyAfterJob(success);

            if (success) {
                execution.setExitStatus(ExitStatus.COMPLETED);
                execution.setStatus(BatchStatus.COMPLETED);
            } else {
                execution.setExitStatus(ExitStatus.FAILED);
                execution.setStatus(BatchStatus.FAILED);
            }
        }
    }

    /**
     * Execute a single job step.
     *
     * @param stepImplementation Object containing information about the step to be performed
     * @param nSteps             Total number of steps for this job
     * @throws InvocationTargetException When the job step throws an exception
     * @throws IllegalAccessException    When the job step cannot be accessed
     */
    private void executeJobStep(JobStepImplementation stepImplementation, int nSteps) throws Exception {

        int position = stepImplementation.getAnnotation().position();
        String stepName = stepImplementation.getAnnotation().value();
        boolean success = true;

        if (this.skipSteps.contains(position)) {
            return;
        }

        try {
            notifyBeforeStep(position, stepName, nSteps);
            invokeStep(stepImplementation);
        } catch (Exception e) {
            e.printStackTrace();
            success = false;
            notifyStepFailed(position, stepName, e);
            throw e;
        } finally {
            notifyAfterStep(position, stepName, success);
        }
    }

    /**
     * Runs a step, giving it the job logger if necessary.
     *
     * @param stepImplementation The step to run
     * @throws InvocationTargetException If there is a problem invoking the method
     * @throws IllegalAccessException    If there is a problem invoking the method
     */
    private void invokeStep(JobStepImplementation stepImplementation)
        throws InvocationTargetException, IllegalAccessException {

        Method method = stepImplementation.getMethod();

        // TODO this is fine now, but if the possible method signatures
        //      ever get more complex this will need to be refactored
        if (method.getParameterCount() == 0) {
            method.invoke(this);
        } else if (method.getParameterCount() == 1) {
            if (method.getParameterTypes()[0].equals(JobLogger.class)) {
                method.invoke(this, dbLogger);
            } else {
                throw new SafaError("Unsure how to invoke method %s of %s. Parameter 1 is not a JobLogger",
                    method.getName(), method.getDeclaringClass().getName());
            }
        } else {
            throw new SafaError("Unsure how to invoke method %s of %s. Too many parameters found",
                method.getName(), method.getDeclaringClass().getName());
        }
    }

    protected abstract UUID getCompletedEntityId();

    @IJobStep(value = "Done", position = -1)
    public void done() {
        this.jobDbEntity.setCompletedEntityId(this.getCompletedEntityId());
        this.serviceProvider.getJobService().completeJob(jobDbEntity);
    }

    /**
     * Broadcast that the job is about to start.
     */
    private void notifyBeforeJob() throws Exception {
        try {
            beforeJob();
        } catch (Exception e) {
            dbLogger.log("Error in reporting job starting");
            throw e;
        }
    }

    /**
     * Broadcast that the job has finished.
     *
     * @param success Whether the job finished successfully or not.
     */
    private void notifyAfterJob(boolean success) {
        try {
            afterJob(success);
        } catch (Exception e) {
            dbLogger.log("Error in reporting job finishing:");
            dbLogger.logException(e);
        }
    }

    /**
     * Broadcast that a step is about to be executed.
     *
     * @param stepPosition The position of the step as defined by its annotation.
     * @param stepName     The name of the step as defined by its annotation.
     * @param nSteps       The number of steps in this job.
     */
    private void notifyBeforeStep(int stepPosition, String stepName, int nSteps) throws Exception {
        try {
            int stepNum = JobExecutionUtilities.getStepIndex(stepPosition, nSteps);
            dbLogger.setStepNum(stepNum);
            jobService.startStep(jobDbEntity, stepNum, nSteps);
            notifyStateChange();

            log.info("Running job step \"{}\"", stepName);

            beforeStep(stepPosition, stepName);
        } catch (Exception e) {
            dbLogger.log("Error in reporting step starting");
            throw e;
        }
    }

    /**
     * Broadcast that a step has completed.
     *
     * @param stepPosition The position of the step as defined by its annotation.
     * @param stepName     The name of the step as defined by its annotation.
     * @param success      Whether the step finished successfully or not.
     */
    private void notifyAfterStep(int stepPosition, String stepName, boolean success) throws Exception {
        try {
            jobService.endStep(jobDbEntity);
            notifyStateChange();

            afterStep(stepPosition, stepName, success);
        } catch (Exception e) {
            dbLogger.log("Error in reporting step finishing");
            throw e;
        }
    }

    /**
     * Broadcast that a step failed.
     *
     * @param stepPosition The position of the step as defined by its annotation.
     * @param stepName     The name of the step as defined by its annotation.
     * @param error        The error that caused the failure.
     */
    private void notifyStepFailed(int stepPosition, String stepName, Exception error) {
        try {
            stepFailed(stepPosition, stepName, error);
        } catch (Exception e) {
            dbLogger.log("Error in reporting step failure:");
            dbLogger.logException(e);
        }
    }

    /**
     * Broadcast that a job failed.
     *
     * @param error The error that caused the failure.
     */
    private void notifyJobFailed(Exception error) {
        try {
            dbLogger.log("Error executing job:");
            dbLogger.logException(error);

            jobService.failJob(jobDbEntity);
            notifyStateChange();

            jobFailed(error);
        } catch (Exception e) {
            dbLogger.log("Additional error in reporting the previous error:");
            dbLogger.logException(e);
        }
    }

    /**
     * Broadcast a change in this job to any clients that are listening for it.
     */
    private void notifyStateChange() {
        notificationService.sendJob(JobAppEntity.createFromJob(jobDbEntity));
    }

    /**
     * <p>Override this method to be notified when this job is about to start.</p>
     *
     * <p>This method is guaranteed to be called before any steps start executing.</p>
     *
     * @throws Exception In case of an error
     */
    @ForOverride
    protected void beforeJob() throws Exception {
    }

    /**
     * <p>Override this method to be notified when this job is finished.</p>
     *
     * <p>This method is guaranteed to be called after all steps are finished executing, or
     * immediately after {@link #jobFailed(Exception)} if the job fails.</p>
     *
     * @param success Whether the job completed successfully or not.
     * @throws Exception In case of an error
     */
    @ForOverride
    protected void afterJob(boolean success) throws Exception {
    }

    /**
     * <p>Override this method to be notified when a step is about to start.</p>
     *
     * @param stepPosition The position of the step as defined by its {@link IJobStep} annotation.
     * @param stepName     The name of the step as defined by its {@link IJobStep} annotation.
     * @throws Exception In case of an error
     */
    @ForOverride
    protected void beforeStep(int stepPosition, String stepName) throws Exception {
    }

    /**
     * <p>Override this method to be notified when a step has completed.</p>
     *
     * <p>In the case of a step failing, this method will always be called after
     * {@link #stepFailed(int, String, Exception)}, but before {@link #jobFailed(Exception)}.</p>
     *
     * @param stepPosition The position of the step as defined by its {@link IJobStep} annotation.
     * @param stepName     The name of the step as defined by its {@link IJobStep} annotation.
     * @param success      Whether the step completed successfully or not.
     * @throws Exception In case of an error
     */
    @ForOverride
    protected void afterStep(int stepPosition, String stepName, boolean success) throws Exception {
    }

    /**
     * <p>Override this method to be notified when a step fails.</p>
     *
     * <p>This will be called before {@link #afterStep(int, String, boolean)} as well
     * as before {@link #jobFailed(Exception)} and {@link #afterJob(boolean)}</p>
     *
     * @param stepPosition The position of the step as defined by its {@link IJobStep} annotation.
     * @param stepName     The name of the step as defined by its {@link IJobStep} annotation.
     * @param error        The error that caused the step to fail.
     * @throws Exception In case of an error
     */
    @ForOverride
    protected void stepFailed(int stepPosition, String stepName, Exception error) throws Exception {
    }

    /**
     * <p>Override this method to be notified when a job fails.</p>
     *
     * <p>This is called after {@link #afterStep(int, String, boolean)} but before {@link #afterJob(boolean)}.</p>
     *
     * @param error The error that caused the job to fail.
     * @throws Exception In case of an error
     */
    @ForOverride
    protected void jobFailed(Exception error) throws Exception {
    }

    @Override
    @NonNull
    public String getName() {
        return this.jobDbEntity.getName();
    }

    @Override
    public boolean isRestartable() {
        return false;
    }

    @Override
    public JobParametersIncrementer getJobParametersIncrementer() {
        return params -> Objects.requireNonNullElseGet(params, JobParameters::new);
    }

    @Override
    @NonNull
    public JobParametersValidator getJobParametersValidator() {
        return params -> {
        };
    }
}
