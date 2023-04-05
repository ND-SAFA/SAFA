package edu.nd.crc.safa.features.jobs;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobStepImplementation;

public interface JobExecutionUtilities {
    /**
     * Returns list of job steps including their position, name, and method implementation.
     *
     * @param jobClass The job class to retrieve steps for.
     * @param <T>      The class of the job.
     * @return List of {@link JobStepImplementation} for job class.
     */
    static <T extends AbstractJob> List<JobStepImplementation> getSteps(Class<T> jobClass) {
        List<JobStepImplementation> jobSteps = new ArrayList<>();
        for (Method method : jobClass.getMethods()) {
            IJobStep jobStep = method.getAnnotation(IJobStep.class);
            if (jobStep != null) {
                JobStepImplementation stepImplementation = new JobStepImplementation(jobStep, method);
                jobSteps.add(stepImplementation);
            }
        }

        JobStepImplementation[] stepImpls = new JobStepImplementation[jobSteps.size()];
        for (JobStepImplementation stepImplementation : jobSteps) {
            int position = stepImplementation.getAnnotation().position();
            int index = getStepIndex(position, jobSteps.size());
            stepImpls[index] = stepImplementation;
        }
        return Arrays.asList(stepImpls);
    }

    /**
     * Returns names of steps of given abstract job class.
     *
     * @param jobClass Job to retrieve step names from.
     * @param <T>      The type of Abstract job.
     * @return List of string names representing job steps.
     */
    static <T extends AbstractJob> List<String> getJobStepNames(Class<T> jobClass) {
        return getSteps(jobClass)
            .stream()
            .map(jobStepImplementation -> jobStepImplementation.getAnnotation().value())
            .collect(Collectors.toList());
    }

    static int getStepIndex(int position, int size) {
        if (position > 0) {
            return position - 1;
        } else {
            return size + position;
        }
    }
}
