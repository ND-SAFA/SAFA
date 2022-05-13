package edu.nd.crc.safa.config;

import edu.nd.crc.safa.server.services.jira.JiraConnectionService;
import edu.nd.crc.safa.server.services.jira.JiraConnectionServiceImpl;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Responsible for configuring the jira connection service
 * implementation for the application.
 */
@Configuration
public class JiraConfiguration {
    @Bean
    public JiraConnectionService jiraConnectionService() {
        return new JiraConnectionServiceImpl();
    }
}
