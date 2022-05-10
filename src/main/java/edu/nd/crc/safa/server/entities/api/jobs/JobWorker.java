package edu.nd.crc.safa.server.entities.api.jobs;

import java.io.IOException;
import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.JobSteps;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.services.JobService;
import edu.nd.crc.safa.server.services.NotificationService;

import org.springframework.batch.core.Job;
import org.springframework.batch.core.JobExecution;
import org.springframework.batch.core.JobParametersIncrementer;
import org.springframework.batch.core.JobParametersValidator;
import org.springframework.scheduling.annotation.Async;

/**
 * Uses reflection to parse and run steps
 */
public abstract class JobWorker implements Job {

    /**
     * The job identifying information that is being performed.
     */
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

    public JobDbEntity getJob() {
        return jobDbEntity;
    }

    public void setJob(JobDbEntity jobDbEntity) {
        this.jobDbEntity = jobDbEntity;
    }

    @Override
    @Async
    public void execute(JobExecution execution) {
        try {
            this.initJobData();
        } catch (Exception e) {
            this.jobService.failJob(jobDbEntity);
            throw new RuntimeException(e);
        }
        String[] stepNames = JobSteps.getJobSteps(this.jobDbEntity.getJobType());
        for (int i = 0; i < stepNames.length; i++) {
            try {
                Method method = getMethodForStepByName(stepNames[i]);
                boolean isLastStep = i == stepNames.length - 1;

                // Step - Mark step as started and update
                this.jobService.startStep(jobDbEntity);
                this.notificationService.broadUpdateJobMessage(jobDbEntity);

                //TODO: Remove this after testing
                Thread.sleep(1 * 1000);

                method.invoke(this);

                // Step - Mark step as done and broadcast.
                if (isLastStep) {
                    this.onComplete();
                } else {
                    this.jobService.endStep(jobDbEntity);
                }
                this.notificationService.broadUpdateJobMessage(jobDbEntity);

            } catch (Exception e) {
                this.jobService.failJob(jobDbEntity);
                e.printStackTrace();
                throw new RuntimeException(e);
            }
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
            throw new RuntimeException("Could not find implementation for step: " + stepName);
        } else if (methodQuery.size() == 1) {
            return methodQuery.get(0);
        } else {
            List<String> methodNames = methodQuery.stream().map(Method::getName).collect(Collectors.toList());
            String error = String.format("Found more than one implementation for step: %s\n%s", stepName, methodNames);
            throw new RuntimeException(error);
        }
    }

    protected void onComplete() {
        this.jobService.completeJob(jobDbEntity);
    }

    /**
     * Responsible for initializing any data needed to run the job steps.
     *
     * @throws SafaError   Error occurring during job initialization.
     * @throws IOException Error occurring during
     */
    public void initJobData() throws SafaError {
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
        return (params) -> params;
    }

    @Override
    public JobParametersValidator getJobParametersValidator() {
        return (params) -> {
        };
    }

}
