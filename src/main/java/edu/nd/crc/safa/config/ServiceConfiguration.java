package edu.nd.crc.safa.config;

import edu.nd.crc.safa.server.services.jira.JiraConnectionService;
import edu.nd.crc.safa.server.services.jira.JiraConnectionServiceImpl;
import edu.nd.crc.safa.utilities.ExecutorDelegate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;


/**
 * Bean definition for services
 */
@Configuration
public class ServiceConfiguration {

    @Value("${task-executor.controller.core-pool-size}")
    private int controllerCorePoolSize;

    @Value("${task-executor.controller.max-pool-size}")
    private int controllerMaxPoolSize;

    @Bean
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

    @Bean
    public JiraConnectionService jiraConnectionService() {
        return new JiraConnectionServiceImpl();
    }
}
