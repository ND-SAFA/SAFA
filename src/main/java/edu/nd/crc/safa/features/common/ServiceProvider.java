package edu.nd.crc.safa.features.common;

import edu.nd.crc.safa.authentication.TokenService;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.attributes.services.AttributeLayoutService;
import edu.nd.crc.safa.features.attributes.services.AttributeService;
import edu.nd.crc.safa.features.attributes.services.AttributeValueService;
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
import edu.nd.crc.safa.features.generation.api.GenApi;
import edu.nd.crc.safa.features.generation.hgen.HGenService;
import edu.nd.crc.safa.features.generation.projectsummary.ProjectSummaryService;
import edu.nd.crc.safa.features.generation.search.SearchService;
import edu.nd.crc.safa.features.generation.summary.SummaryService;
import edu.nd.crc.safa.features.generation.tgen.services.TraceGenerationService;
import edu.nd.crc.safa.features.github.repositories.GithubAccessCredentialsRepository;
import edu.nd.crc.safa.features.github.repositories.GithubProjectRepository;
import edu.nd.crc.safa.features.github.services.GithubConnectionService;
import edu.nd.crc.safa.features.github.services.GithubGraphQlService;
import edu.nd.crc.safa.features.jira.repositories.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.features.jira.repositories.JiraProjectRepository;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.jira.services.JiraParsingService;
import edu.nd.crc.safa.features.jobs.logging.services.JobLoggingService;
import edu.nd.crc.safa.features.jobs.repositories.JobDbRepository;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.layout.repositories.ArtifactPositionRepository;
import edu.nd.crc.safa.features.layout.services.ArtifactPositionService;
import edu.nd.crc.safa.features.memberships.repositories.UserProjectMembershipRepository;
import edu.nd.crc.safa.features.memberships.services.MemberService;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.projects.services.ProjectRetrievalService;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.rules.repositories.RuleRepository;
import edu.nd.crc.safa.features.rules.services.RuleService;
import edu.nd.crc.safa.features.rules.services.WarningService;
import edu.nd.crc.safa.features.traces.ITraceGenerationController;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkRepository;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.features.traces.services.TraceMatrixService;
import edu.nd.crc.safa.features.traces.services.TraceService;
import edu.nd.crc.safa.features.types.services.TypeService;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;
import edu.nd.crc.safa.features.users.services.AccountLookupService;
import edu.nd.crc.safa.features.users.services.DefaultProjectCreatorService;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.features.versions.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.features.versions.services.VersionService;
import edu.nd.crc.safa.utilities.ExecutorDelegate;
import edu.nd.crc.safa.utilities.graphql.services.GraphQlService;

import jakarta.annotation.PostConstruct;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;
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
    @Getter
    private static ServiceProvider instance;
    // Project
    private final ProjectRepository projectRepository;
    private final ProjectService projectService;
    private final ProjectRetrievalService projectRetrievalService;
    private final ProjectSummaryService projectSummaryService;
    // Members
    private final UserProjectMembershipRepository userProjectMembershipRepository;
    private final MemberService memberService;
    // Versions
    private final VersionService versionService;
    // Types
    private final TypeService typeService;
    // Artifact
    private final ArtifactRepository artifactRepository;
    private final ArtifactPositionRepository artifactPositionRepository;
    private final ArtifactVersionRepository artifactVersionRepository;
    private final ArtifactService artifactService;
    // Custom Attributes
    private final AttributeService attributeService;
    private final AttributeValueService attributeValueService;
    private final AttributeLayoutService attributeLayoutService;
    //Traces
    private final ITraceGenerationController traceGenerationController;
    private final TraceLinkVersionRepository traceLinkVersionRepository;
    private final TraceService traceService;
    private final TraceGenerationService traceGenerationService;
    private final TraceLinkRepository traceLinkRepository;
    private final TraceMatrixService traceMatrixService;
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
    private final DefaultProjectCreatorService defaultProjectCreatorService;
    // HTTP
    private final RequestService requestService;
    private final GraphQlService graphQlService;
    private final GenApi genApi;
    // GitHub
    private final GithubAccessCredentialsRepository githubAccessCredentialsRepository;
    private final GithubConnectionService githubConnectionService;
    private final GithubProjectRepository githubProjectRepository;
    private final GithubGraphQlService githubGraphQlService;
    private final JobService jobService;
    private final JobDbRepository jobRepository;
    // Jobs
    private JobLauncher jobLauncher; // Not final because runtime changes on test vs dev.
    private JobLoggingService jobLoggingService;
    // Search
    private SearchService searchService;
    // Summarize
    private SummaryService summaryService;
    // HGen
    private HGenService hGenService;

    @PostConstruct
    public void postInit() {
        ServiceProvider.instance = this;
    }
}
