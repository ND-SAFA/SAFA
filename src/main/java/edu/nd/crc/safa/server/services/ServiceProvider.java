package edu.nd.crc.safa.server.services;

import edu.nd.crc.safa.importer.flatfiles.FlatFileService;
import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.repositories.CommitErrorRepository;
import edu.nd.crc.safa.server.repositories.jira.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.server.services.jira.JiraConnectionService;
import edu.nd.crc.safa.server.services.jobs.JobService;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import org.springframework.batch.core.launch.JobLauncher;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
@Getter
@Setter
@Scope("singleton")
public class ServiceProvider {
    // Flat Files
    private final ProjectService projectService;
    private final FileUploadService fileUploadService;
    private final FlatFileService flatFileService;
    private final EntityVersionService entityVersionService;
    private final AppEntityRetrievalService appEntityRetrievalService;
    // Common
    private final NotificationService notificationService;
    private final JobService jobService;
    private final SafaUserService safaUserService;
    private final CommitErrorRepository commitErrorRepository;
    // JIRA
    private final JiraAccessCredentialsRepository jiraAccessCredentialsRepository;
    private final JiraConnectionService jiraConnectionService;
    // Jobs
    JobLauncher jobLauncher;
}
