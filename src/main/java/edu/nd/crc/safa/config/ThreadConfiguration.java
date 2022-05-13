package edu.nd.crc.safa.config;

import edu.nd.crc.safa.utilities.ExecutorDelegate;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;


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
}
