package edu.nd.crc.safa.server.services;

import edu.nd.crc.safa.importer.flatfiles.ArtifactFileParser;
import edu.nd.crc.safa.importer.flatfiles.FlatFileService;
import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.repositories.CommitErrorRepository;
import edu.nd.crc.safa.server.repositories.github.GithubAccessCredentialsRepository;
import edu.nd.crc.safa.server.repositories.github.GithubProjectRepository;
import edu.nd.crc.safa.server.repositories.jira.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.server.services.github.GithubConnectionService;
import edu.nd.crc.safa.server.services.jira.JiraConnectionService;
import edu.nd.crc.safa.server.services.jobs.JobService;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.batch.core.launch.JobLauncher;
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
    private final FileUploadService fileUploadService;
    private final FlatFileService flatFileService;
    private final EntityVersionService entityVersionService;
    private final AppEntityRetrievalService appEntityRetrievalService;
    private final ArtifactFileParser artifactFileParser;
    // Common
    private final NotificationService notificationService;
    private final JobService jobService;
    private final SafaUserService safaUserService;
    private final CommitErrorRepository commitErrorRepository;
    // JIRA
    private final JiraAccessCredentialsRepository jiraAccessCredentialsRepository;
    private final JiraConnectionService jiraConnectionService;
    // Jobs
    private final JobLauncher jobLauncher;
    // GitHub
    private final GithubAccessCredentialsRepository githubAccessCredentialsRepository;
    private final GithubConnectionService githubConnectionService;
    private final GithubProjectRepository githubProjectRepository;
}
