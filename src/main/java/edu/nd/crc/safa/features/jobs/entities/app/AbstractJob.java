package edu.nd.crc.safa.features.jobs.entities.app;

import java.io.IOException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
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

    /**
     * The job identifying information that is being performed.
     */
    JobDbEntity jobDbEntity;
    /**
     * Service used to send job updates.
     */
    ServiceProvider serviceProvider;
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
            .map(jobStepImplementation -> jobStepImplementation.annotation.name())
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
    public void execute(JobExecution execution) {
        JobService jobService = this.serviceProvider.getJobService();
        NotificationService notificationService = this.serviceProvider.getNotificationService();

        List<JobStepImplementation> jobSteps = getSteps(this.getClass());
        int nSteps = jobSteps.size();

        try {
            for (JobStepImplementation stepImplementation : jobSteps) {
                if (this.skipSteps.contains(stepImplementation.annotation.position())) {
                    continue;
                }
                // Pre-step
                jobService.startStep(jobDbEntity, nSteps);
                notificationService.broadcastJob(JobAppEntity.createFromJob(jobDbEntity));

                // Pre-step
                stepImplementation.method.invoke(this);

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

    @IJobStep(name = "Done", position = -1)
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
