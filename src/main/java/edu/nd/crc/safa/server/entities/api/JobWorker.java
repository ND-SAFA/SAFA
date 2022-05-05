package edu.nd.crc.safa.server.entities.api;

import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.entities.app.JobSteps;
import edu.nd.crc.safa.server.entities.db.Job;
import edu.nd.crc.safa.server.services.JobService;
import edu.nd.crc.safa.server.services.NotificationService;

/**
 * Uses reflection to parse and run steps
 */
public abstract class JobWorker extends Thread {

    private static final String STEP_KEYWORD = "step";

    /**
     * The job identifying information that is being performed.
     */
    Job job;

    /**
     * The service object for modifying job instance.
     */
    JobService jobService;

    /**
     * Service used to send job updates.
     */
    NotificationService notificationService;

    public JobWorker(Job job, JobService jobService, NotificationService notificationService) {
        this.job = job;
        this.jobService = jobService;
        this.notificationService = notificationService;
    }

    public Job getJob() {
        return job;
    }

    public void setJob(Job job) {
        this.job = job;
    }

    public void run() {
        String[] stepNames = JobSteps.getJobSteps(this.job.getJobType());
        for (int i = 0; i < stepNames.length; i++) {
            try {
                Method method = getMethodFromStep(stepNames[i]);
                boolean isLastStep = i == stepNames.length - 1;

                // Step - Mark step as started and update
                this.jobService.startStep(job);
                this.notificationService.broadUpdateJobMessage(job);

                method.invoke(this);

                // Step - Mark step as done and broadcast.
                this.jobService.endStep(job);
                this.notificationService.broadUpdateJobMessage(job);

                if (isLastStep) {
                    this.onComplete();
                }
            } catch (Exception e) {
                e.printStackTrace();
                throw new RuntimeException(e);
            }
        }
    }

    public Method getMethodFromStep(String stepName) {
        String query = stepName.replace(" ", "").toLowerCase();
        List<Method> methodQuery = Arrays
            .stream(this.getClass().getDeclaredMethods())
            .filter(m -> m.getName().toLowerCase().contains(query))
            .collect(Collectors.toList());
        int methodQuerySize = methodQuery.size();

        if (methodQuerySize == 0) {
            throw new RuntimeException("Could not find implementation for step: " + stepName);
        } else if (methodQuery.size() == 1) {
            return methodQuery.get(0);
        } else {
            String error = String.format("Found more than one implementation for step: %s\n%s", stepName, methodQuery);
            throw new RuntimeException(error);
        }
    }

    protected void onComplete() {
        this.jobService.completeJob(job);
    }
}
