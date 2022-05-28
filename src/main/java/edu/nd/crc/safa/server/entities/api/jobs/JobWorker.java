package edu.nd.crc.safa.server.entities.api.jobs;

import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.JobSteps;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.services.JobService;
import edu.nd.crc.safa.server.services.NotificationService;

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
public abstract class JobWorker implements Job {

    /**
     * The job identifying information that is being performed.
     */
    @Getter
    @Setter
    JobDbEntity jobDbEntity;
    /**
     * The service object for modifying job instance.
     */
    JobService jobService;
    /**
     * Service used to send job updates.
     */
    NotificationService notificationService;

    public JobWorker(JobDbEntity jobDbEntity) {
        this.jobDbEntity = jobDbEntity;
        this.jobService = JobService.getInstance();
        this.notificationService = NotificationService.getInstance();
    }

    @Override
    public void execute(JobExecution execution) {
        String[] stepNames = JobSteps.getJobSteps(this.jobDbEntity.getJobType());
        for (String stepName : stepNames) {
            try {
                // Pre-step
                Thread.sleep(500);
                Method method = getMethodForStepByName(stepName);
                this.jobService.startStep(jobDbEntity);
                this.notificationService.broadUpdateJobMessage(jobDbEntity);

                // Step
                method.invoke(this);

                // Post-step
                this.jobService.endStep(jobDbEntity);
                this.notificationService.broadUpdateJobMessage(jobDbEntity);
            } catch (Exception e) {
                this.jobService.failJob(jobDbEntity);
                e.printStackTrace();
                this.notificationService.broadUpdateJobMessage(jobDbEntity);
                throw new RuntimeException(e);
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
            throw new RuntimeException("Could not find implementation for step: " + stepName);
        } else if (methodQuery.size() == 1) {
            return methodQuery.get(0);
        } else {
            List<String> methodNames = methodQuery.stream().map(Method::getName).collect(Collectors.toList());
            String error = String.format("Found more than one implementation for step: %s\n%s", stepName, methodNames);
            throw new RuntimeException(error);
        }
    }

    public void done() {
        this.jobService.completeJob(jobDbEntity);
    }

    /**
     * Responsible for initializing any data needed to run the job steps.
     *
     * @throws SafaError Error occurring during job initialization.
     */
    public void initJobData() throws SafaError {
    }

    @Override
    @NotNull
    public String getName() {
        return this.jobDbEntity.getName();
    }

    @Override
    public boolean isRestartable() {
        return false;
    }

    @Override
    public JobParametersIncrementer getJobParametersIncrementer() {
        return (params) -> params;
    }

    @Override
    public JobParametersValidator getJobParametersValidator() {
        return (params) -> {
        };
    }
}
