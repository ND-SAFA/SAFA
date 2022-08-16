package edu.nd.crc.safa.features.common;

import edu.nd.crc.safa.features.commits.services.EntityVersionService;
import edu.nd.crc.safa.features.errors.repositories.CommitErrorRepository;
import edu.nd.crc.safa.features.flatfiles.services.FileUploadService;
import edu.nd.crc.safa.features.flatfiles.services.FlatFileService;
import edu.nd.crc.safa.features.jira.repositories.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.notifications.NotificationService;
import edu.nd.crc.safa.features.projects.services.AppEntityRetrievalService;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.features.versions.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.repositories.github.GithubAccessCredentialsRepository;
import edu.nd.crc.safa.server.repositories.github.GithubProjectRepository;
import edu.nd.crc.safa.server.services.github.GithubConnectionService;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.batch.core.launch.JobLauncher;
import org.springframework.batch.core.launch.support.SimpleJobLauncher;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

/**
 * Encapsulates series of services used during job execution.
 * This abstraction allows us to only have to pass a single service (ServiceProvider)
 * to have access to all Spring Boot services outside of its component ecosystem,
 * like a job.
 */
@Component
@AllArgsConstructor
@Data
@Scope("singleton")
public class ServiceProvider {
    // Flat Files
    private final ProjectService projectService;
    private final ProjectVersionRepository projectVersionRepository;
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
    // Jobs(not final since is set while testing)
    private JobLauncher jobLauncher;
    // GitHub
    private final GithubAccessCredentialsRepository githubAccessCredentialsRepository;
    private final GithubConnectionService githubConnectionService;
    private final GithubProjectRepository githubProjectRepository;
}
