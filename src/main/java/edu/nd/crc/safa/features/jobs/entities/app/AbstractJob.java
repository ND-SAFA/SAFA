package edu.nd.crc.safa.features.jobs.entities.app;

import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NonNull;
import lombok.Setter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.batch.core.Job;
import org.springframework.batch.core.JobExecution;
import org.springframework.batch.core.JobParametersIncrementer;
import org.springframework.batch.core.JobParametersValidator;

/**
 * Responsible for finding methods corresponding to steps in job and running them
 * by providing a default execution method.
 *
 * <p>TODO: Create annotation to specify step implementations over reflection.
 */
@Getter
@Setter
public abstract class AbstractJob implements Job {

    private static final Logger log = LoggerFactory.getLogger(AbstractJob.class);

    /**
     * The job identifying information that is being performed.
     */
    protected JobDbEntity jobDbEntity;
    /**
     * Service used to send job updates.
     */
    protected ServiceProvider serviceProvider;
    /**
     * List of step indices to skip.
     */
    List<Integer> skipSteps = new ArrayList<>();

    protected AbstractJob(JobDbEntity jobDbEntity, ServiceProvider serviceProvider) {
        this.jobDbEntity = jobDbEntity;
        this.serviceProvider = serviceProvider;
    }

    /**
     * Returns list of job steps including their position, name, and method implementation.
     *
     * @param jobClass The job class to retrieve steps for.
     * @param <T>      The class of of the job.
     * @return List of {@link JobStepImplementation} for job class.
     */
    static <T extends AbstractJob> List<JobStepImplementation> getSteps(Class<T> jobClass) {
        List<JobStepImplementation> jobSteps = new ArrayList<>();
        for (Method method : jobClass.getMethods()) {
            IJobStep jobStep = method.getAnnotation(IJobStep.class);
            if (jobStep != null) {
                JobStepImplementation stepImplementation = new JobStepImplementation(
                    jobStep,
                    method
                );
                jobSteps.add(stepImplementation);
            }
        }

        JobStepImplementation[] stepNames = new JobStepImplementation[jobSteps.size()];
        for (JobStepImplementation stepImplementation : jobSteps) {
            int position = stepImplementation.annotation.position();
            int index = getStepIndex(position, jobSteps.size());
            stepNames[index] = stepImplementation;
        }
        return Arrays.asList(stepNames);
    }

    /**
     * Returns names of steps of given abstract job class.
     *
     * @param jobClass Job to retrieve step names from.
     * @param <T>      The type of Abstract job.
     * @return List of string names representing job steps.
     */
    static <T extends AbstractJob> List<String> getJobSteps(Class<T> jobClass) {
        return getSteps(jobClass)
            .stream()
            .map(jobStepImplementation -> jobStepImplementation.annotation.value())
            .collect(Collectors.toList());
    }

    public static int getStepIndex(int position, int size) {
        if (position > 0) {
            return position - 1;
        } else {
            return size + position;
        }
    }

    /**
     * For job steps updating the job status as the steps progress.
     *
     * @param execution JobExecution used for restarting jobs (WIP).
     */
    @Override
    public void execute(@NonNull JobExecution execution) {
        JobService jobService = this.serviceProvider.getJobService();
        NotificationService notificationService = this.serviceProvider.getNotificationService();

        List<JobStepImplementation> jobSteps = getSteps(this.getClass());
        int nSteps = jobSteps.size();

        JobLogger logger = new JobLogger(serviceProvider.getJobLoggingService(), jobDbEntity, 0);

        try {
            for (JobStepImplementation stepImplementation : jobSteps) {
                if (this.skipSteps.contains(stepImplementation.annotation.position())) {
                    continue;
                }
                // Pre-step
                logger.setStepNum(stepImplementation.annotation.position());
                jobService.startStep(jobDbEntity, nSteps);
                notificationService.broadcastJob(JobAppEntity.createFromJob(jobDbEntity));

                // Pre-step
                log.info("Running job step " + stepImplementation.method.getName());
                invokeStep(stepImplementation, logger);

                // Post-step
                jobService.endStep(jobDbEntity);
                notificationService.broadcastJob(JobAppEntity.createFromJob(jobDbEntity));
            }
        } catch (Exception e) {
            jobService.failJob(jobDbEntity);
            e.printStackTrace();
            notificationService.broadcastJob(JobAppEntity.createFromJob(jobDbEntity));
            throw new SafaError(e.getMessage());
        }

        this.done();
    }

    /**
     * Runs a step, giving it the job logger if necessary.
     *
     * @param stepImplementation The step to run
     * @param logger The logger to give to the step if it wants it
     * @throws InvocationTargetException If there is a problem invoking the method
     * @throws IllegalAccessException If there is a problem invoking the method
     */
    private void invokeStep(JobStepImplementation stepImplementation, JobLogger logger)
            throws InvocationTargetException, IllegalAccessException {

        Method method = stepImplementation.method;

        // TODO this is fine now, but if the possible method signatures ever get more complex this will need to be refactored
        if (method.getParameterCount() == 0) {
            method.invoke(this);
        } else if (method.getParameterCount() == 1) {
            if (method.getParameterTypes()[0].equals(JobLogger.class)) {
                method.invoke(this, logger);
            } else {
                throw new SafaError("Unsure how to invoke method %s of %s. Parameter 1 is not a JobLogger",
                        method.getName(), method.getDeclaringClass().getName());
            }
        } else {
            throw new SafaError("Unsure how to invoke method %s of %s. Too many parameters found",
                    method.getName(), method.getDeclaringClass().getName());
        }
    }

    /**
     * Returns the method responsible for running step with given name.
     * Name is matches step if lower case versions of each match.
     *
     * @param stepName The name of the step to retrieve method for.
     * @return The method matching given step name.
     */
    public Method getMethodForStepByName(String stepName) {
        String query = stepName.replace(" ", "").toLowerCase();
        List<Method> methodQuery = Arrays
            .stream(this.getClass().getMethods())
            .filter(m -> m.getName().toLowerCase().contains(query))
            .collect(Collectors.toList());
        int methodQuerySize = methodQuery.size();

        if (methodQuerySize == 0) {
            throw new SafaError("Could not find implementation for step: " + stepName);
        } else if (methodQuery.size() == 1) {
            return methodQuery.get(0);
        } else {
            List<String> methodNames = methodQuery.stream().map(Method::getName).collect(Collectors.toList());
            String error = String.format("Found more than one implementation for step: %s%n%s", stepName, methodNames);
            throw new SafaError(error);
        }
    }

    protected abstract UUID getCompletedEntityId();

    @IJobStep(value = "Done", position = -1)
    public void done() {
        this.jobDbEntity.setCompletedEntityId(this.getCompletedEntityId());
        this.serviceProvider.getJobService().completeJob(jobDbEntity);
    }

    /**
     * Responsible for initializing any data needed to run the job steps.
     *
     * @throws SafaError Error occurring during job initialization.
     */
    public void initJobData() throws SafaError, IOException {
    }

    @Override
    public String getName() {
        return this.jobDbEntity.getName();
    }

    @Override
    public boolean isRestartable() {
        return false;
    }

    @Override
    public JobParametersIncrementer getJobParametersIncrementer() {
        return params -> params;
    }

    @Override
    public JobParametersValidator getJobParametersValidator() {
        return params -> {
        };
    }

    @AllArgsConstructor
    static class JobStepImplementation {
        IJobStep annotation;
        Method method;
    }
}
