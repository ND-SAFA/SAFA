package edu.nd.crc.safa.config;

import org.springframework.batch.core.launch.JobLauncher;
import org.springframework.batch.core.launch.support.TaskExecutorJobLauncher;
import org.springframework.batch.core.repository.JobRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.context.annotation.Scope;
import org.springframework.core.task.SimpleAsyncTaskExecutor;

/**
 * Configures application to allow batch jobs to be processed asynchronously.
 */
@Configuration
public class BatchConfiguration {

    @Autowired
    private JobRepository jobRepository;

    /**
     * Sets the current task executor to run jobs asynchronously.
     * Note, this is overwritten in SprintBootBaseTest to use a synchronous one for testing.
     *
     * @return JobLauncher
     * @throws Exception Throws exception on afterPropertiesSet if incompatibilities detected.
     */
    @Bean
    @Primary
    @Scope("singleton")
    public JobLauncher simpleAsyncJobLauncher() throws Exception {
        TaskExecutorJobLauncher jobLauncher = new TaskExecutorJobLauncher();
        jobLauncher.setJobRepository(jobRepository);
        jobLauncher.setTaskExecutor(new SimpleAsyncTaskExecutor());
        jobLauncher.afterPropertiesSet();
        return jobLauncher;
    }
}
