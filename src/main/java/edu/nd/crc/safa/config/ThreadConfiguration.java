package edu.nd.crc.safa.config;

import javax.annotation.PostConstruct;

import edu.nd.crc.safa.utilities.ExecutorDelegate;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.security.core.context.SecurityContextHolder;


/**
 * Configures the threads used to serve the requests
 * to the server.
 */
@Configuration
public class ThreadConfiguration {

    @Value("${task-executor.controller.core-pool-size}")
    private int controllerCorePoolSize;
    @Value("${task-executor.controller.max-pool-size}")
    private int controllerMaxPoolSize;

    @Bean
    @Primary
    public ThreadPoolTaskExecutor controllerExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();

        executor.setCorePoolSize(controllerCorePoolSize);
        executor.setMaxPoolSize(controllerMaxPoolSize);
        executor.initialize();

        return executor;
    }

    @Bean
    public ExecutorDelegate executorDelegate() {
        return new ExecutorDelegate(controllerExecutor());
    }

    /**
     * Forces the security context to be copied to child threads (e.g. jobs).
     * Specifically, this allows jobs to have access to the credentials of the
     * user who submitted the job.
     */
    @PostConstruct
    public void setSecurityContextMode() {
        // Only call this method once, otherwise the strategy will reset to default
        SecurityContextHolder.setStrategyName(SecurityContextHolder.MODE_INHERITABLETHREADLOCAL);
    }
}
