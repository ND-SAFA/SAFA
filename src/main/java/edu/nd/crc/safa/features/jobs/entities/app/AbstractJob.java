package edu.nd.crc.safa.features.jobs.entities.app;

import java.io.IOException;
import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

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

    protected AbstractJob(JobDbEntity jobDbEntity, ServiceProvider serviceProvider) {
        this.jobDbEntity = jobDbEntity;
        this.serviceProvider = serviceProvider;
    }

    @Override
    public void execute(JobExecution execution) {
        JobService jobService = this.serviceProvider.getJobService();
        NotificationService notificationService = this.serviceProvider.getNotificationService();
        String[] stepNames = JobSteps.getJobSteps(this.jobDbEntity.getJobType());
        for (String stepName : stepNames) {
            try {
                // Pre-step
                Method method = getMethodForStepByName(stepName);
                jobService.startStep(jobDbEntity);
                notificationService.broadcastChange(EntityChangeBuilder.createJobUpdate(jobDbEntity));

                // Step
                method.invoke(this);

                // Post-step
                jobService.endStep(jobDbEntity);
                notificationService.broadcastChange(EntityChangeBuilder.createJobUpdate(jobDbEntity));
            } catch (Exception e) {
                jobService.failJob(jobDbEntity);
                e.printStackTrace();
                notificationService.broadcastChange(EntityChangeBuilder.createJobUpdate(jobDbEntity));
                throw new SafaError(e.getMessage());
            }
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

    public void done() {
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
}
