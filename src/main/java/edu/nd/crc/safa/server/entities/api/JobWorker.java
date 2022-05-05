package edu.nd.crc.safa.server.entities.api;

import java.lang.reflect.Method;
import java.util.Hashtable;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.entities.db.Job;
import edu.nd.crc.safa.server.services.JobService;
import edu.nd.crc.safa.server.services.NotificationService;
import edu.nd.crc.safa.utilities.MethodNameParser;

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
        List<Method> classMethods = this.getStepMethods();
        for (int i = 0; i < classMethods.size(); i++) {
            try {
                Method method = classMethods.get(i);
                boolean isLastStep = i == classMethods.size() - 1;

                // Step - Mark step as started and update
                this.jobService.startStep(job);
                this.notificationService.broadUpdateJobMessage(job);

                method.invoke(this);

                // Step - Mark step as done and broadcast.
                this.jobService.endStep(job);
                this.notificationService.broadUpdateJobMessage(job);

                if (isLastStep) {
                    this.jobService.completeJob(job);
                }
            } catch (Exception e) {
                e.printStackTrace();
                throw new RuntimeException(e);
            }
        }
    }

    public List<String> getStepNames() {
        return this.getStepMethods().stream().map(Method::getName).collect(Collectors.toList());
    }

    private List<Method> getStepMethods() {
        Hashtable<Integer, Method> stepTable = new Hashtable<>();
        for (Method method : this.getClass().getDeclaredMethods()) {
            if (method.getName().startsWith(STEP_KEYWORD)) {
                int stepNumber = MethodNameParser.getNumberAfterPrefix(method.getName(), STEP_KEYWORD);
                stepTable.put(stepNumber, method);
            }
        }
        return List.copyOf(stepTable.values());
    }
}
