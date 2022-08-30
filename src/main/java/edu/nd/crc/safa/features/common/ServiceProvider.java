package edu.nd.crc.safa.features.common;

import edu.nd.crc.safa.authentication.TokenService;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepositoryImpl;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.delta.services.DeltaService;
import edu.nd.crc.safa.features.documents.repositories.DocumentArtifactRepository;
import edu.nd.crc.safa.features.documents.repositories.DocumentRepository;
import edu.nd.crc.safa.features.documents.services.CurrentDocumentService;
import edu.nd.crc.safa.features.documents.services.DocumentService;
import edu.nd.crc.safa.features.errors.repositories.CommitErrorRepository;
import edu.nd.crc.safa.features.flatfiles.services.CheckArtifactNameService;
import edu.nd.crc.safa.features.flatfiles.services.FileDownloadService;
import edu.nd.crc.safa.features.flatfiles.services.FileUploadService;
import edu.nd.crc.safa.features.flatfiles.services.FlatFileService;
import edu.nd.crc.safa.features.flatfiles.services.ZipFileService;
import edu.nd.crc.safa.features.jira.repositories.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.features.jira.repositories.JiraProjectRepository;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.jira.services.JiraParsingService;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.layout.repositories.ArtifactPositionRepository;
import edu.nd.crc.safa.features.layout.services.ArtifactPositionService;
import edu.nd.crc.safa.features.memberships.repositories.ProjectMembershipRepository;
import edu.nd.crc.safa.features.memberships.services.MemberService;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.projects.services.ProjectRetrievalService;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.rules.repositories.RuleRepository;
import edu.nd.crc.safa.features.rules.services.RuleService;
import edu.nd.crc.safa.features.rules.services.WarningService;
import edu.nd.crc.safa.features.tgen.generator.TraceGenerationService;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkRepository;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.features.traces.repositories.TraceMatrixRepository;
import edu.nd.crc.safa.features.traces.services.TraceService;
import edu.nd.crc.safa.features.types.TypeService;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;
import edu.nd.crc.safa.features.users.services.AccountLookupService;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.features.versions.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.features.versions.services.VersionService;
import edu.nd.crc.safa.features.github.repositories.GithubAccessCredentialsRepository;
import edu.nd.crc.safa.features.github.repositories.GithubProjectRepository;
import edu.nd.crc.safa.features.github.services.GithubConnectionService;
import edu.nd.crc.safa.utilities.ExecutorDelegate;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.batch.core.launch.JobLauncher;
import org.springframework.context.annotation.Scope;
import org.springframework.core.task.TaskExecutor;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.password.PasswordEncoder;
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
    private final ProjectRetrievalService projectRetrievalService;
    // Members
    private final ProjectMembershipRepository projectMembershipRepository;
    private final MemberService memberService;
    // Versions
    private final VersionService versionService;
    // Types
    private final ArtifactTypeRepository artifactTypeRepository;
    private final TypeService typeService;
    // Artifact
    private final ArtifactRepository artifactRepository;
    private final ArtifactPositionRepository artifactPositionRepository;
    private final ArtifactVersionRepository artifactVersionRepository;
    private final ArtifactService artifactService;
    private final ArtifactVersionRepositoryImpl artifactVersionRepositoryImpl;
    //Traces
    private final TraceLinkVersionRepository traceLinkVersionRepository;
    private final TraceService traceService;
    private final TraceGenerationService traceGenerationService;
    private final TraceLinkRepository traceLinkRepository;
    // Matrix
    private final TraceMatrixRepository traceMatrixRepository;
    // Changes
    private final ProjectVersionRepository projectVersionRepository;
    private final CommitErrorRepository commitErrorRepository;
    private final CommitService commitService;
    // Documents
    private final DocumentRepository documentRepository;
    private final DocumentService documentService;
    private final CurrentDocumentService currentDocumentService;
    private final DocumentArtifactRepository documentArtifactRepository;
    // Flat Files
    private final FileUploadService fileUploadService;
    private final FlatFileService flatFileService;
    private final FileDownloadService fileDownloadService;
    private final ZipFileService zipFileService;
    private final CheckArtifactNameService checkArtifactNameService;
    // Notifications
    private final NotificationService notificationService;
    private final SafaUserService safaUserService;
    //Rules
    private final RuleRepository ruleRepository;
    private final RuleService ruleService;
    private final WarningService warningService;
    // JIRA
    private final JiraAccessCredentialsRepository jiraAccessCredentialsRepository;
    private final JiraConnectionService jiraConnectionService;
    private final JobService jobService;
    private final JiraParsingService jiraParsingService;
    private final JiraProjectRepository jiraProjectRepository;
    // Delta
    private final DeltaService deltaService;
    //Layout
    private final ArtifactPositionService artifactPositionService;
    private final TaskExecutor taskExecutor;
    private final ExecutorDelegate executorDelegate;
    // Users
    private final UserDetailsService userDetailsService;
    private final SafaUserRepository safaUserRepository;
    private final AccountLookupService accountLookupService;
    private final TokenService tokenService;
    private final PasswordEncoder passwordEncoder;
    // Jobs(not final since is set while testing)
    private JobLauncher jobLauncher;
    // GitHub
    private final GithubAccessCredentialsRepository githubAccessCredentialsRepository;
    private final GithubConnectionService githubConnectionService;
    private final GithubProjectRepository githubProjectRepository;
}
