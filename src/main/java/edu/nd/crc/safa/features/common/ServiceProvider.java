package edu.nd.crc.safa.features.common;

import edu.nd.crc.safa.features.commits.services.EntityVersionService;
import edu.nd.crc.safa.features.documents.repositories.DocumentRepository;
import edu.nd.crc.safa.features.documents.services.DocumentService;
import edu.nd.crc.safa.features.errors.repositories.CommitErrorRepository;
import edu.nd.crc.safa.features.flatfiles.services.FileUploadService;
import edu.nd.crc.safa.features.flatfiles.services.FlatFileService;
import edu.nd.crc.safa.features.jira.repositories.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.layout.repositories.ArtifactPositionRepository;
import edu.nd.crc.safa.features.layout.services.ArtifactPositionService;
import edu.nd.crc.safa.features.notifications.NotificationService;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.projects.services.AppEntityRetrievalService;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.features.versions.repositories.ProjectVersionRepository;

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
    // Project
    private final ProjectRepository projectRepository;
    private final ProjectService projectService;
    private final AppEntityRetrievalService appEntityRetrievalService;
    // Artifact
    private final ArtifactPositionRepository artifactPositionRepository;
    // Changes
    private final ProjectVersionRepository projectVersionRepository;
    private final EntityVersionService entityVersionService;
    private final CommitErrorRepository commitErrorRepository;
    // Documents
    private final DocumentRepository documentRepository;
    private final DocumentService documentService;
    // Flat Files
    private final FileUploadService fileUploadService;
    private final FlatFileService flatFileService;
    // Notifications
    private final NotificationService notificationService;
    private final SafaUserService safaUserService;
    // JIRA
    private final JiraAccessCredentialsRepository jiraAccessCredentialsRepository;
    private final JiraConnectionService jiraConnectionService;
    private final JobService jobService;
    //Layout
    ArtifactPositionService artifactPositionService;
    // Jobs
    JobLauncher jobLauncher;

}
