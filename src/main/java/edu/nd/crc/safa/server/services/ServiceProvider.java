package edu.nd.crc.safa.server.services;

import edu.nd.crc.safa.importer.flatfiles.FlatFileService;
import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.repositories.jira.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.server.services.jira.JiraConnectionService;
import edu.nd.crc.safa.server.services.jobs.JobService;

import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.batch.core.launch.JobLauncher;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
@Getter
@Scope("singleton")
public class ServiceProvider {
    // Flat Files
    private final ProjectService projectService;
    private final FileUploadService fileUploadService;
    private final FlatFileService flatFileService;
    // Common
    private final NotificationService notificationService;
    private final JobService jobService;
    private final SafaUserService safaUserService;
    // JIRA
    private final JiraAccessCredentialsRepository jiraAccessCredentialsRepository;
    private final JiraConnectionService jiraConnectionService;
    // Jobs
    JobLauncher jobLauncher;
}
