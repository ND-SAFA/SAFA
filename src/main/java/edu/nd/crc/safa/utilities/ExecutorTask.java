package edu.nd.crc.safa.utilities;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import org.springframework.batch.core.JobParametersInvalidException;
import org.springframework.batch.core.repository.JobExecutionAlreadyRunningException;
import org.springframework.batch.core.repository.JobInstanceAlreadyCompleteException;
import org.springframework.batch.core.repository.JobRestartException;

/**
 * No input or output function that might throw {@link Exception}
 */
@FunctionalInterface
public interface ExecutorTask {

    void run() throws SafaError, JobInstanceAlreadyCompleteException, JobExecutionAlreadyRunningException,
        JobParametersInvalidException, JobRestartException;
}
