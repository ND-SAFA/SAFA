package edu.nd.crc.safa.features.common;

import edu.nd.crc.safa.authentication.TokenService;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.billing.services.BillingService;
import edu.nd.crc.safa.features.billing.services.CostEstimationService;
import edu.nd.crc.safa.features.billing.services.TransactionService;
import edu.nd.crc.safa.features.chat.services.ChatMessageService;
import edu.nd.crc.safa.features.chat.services.ChatService;
import edu.nd.crc.safa.features.comments.CommentService;
import edu.nd.crc.safa.features.comments.services.CommentRetrievalService;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.delta.services.DeltaService;
import edu.nd.crc.safa.features.documents.repositories.DocumentArtifactRepository;
import edu.nd.crc.safa.features.documents.repositories.DocumentRepository;
import edu.nd.crc.safa.features.documents.services.CurrentDocumentService;
import edu.nd.crc.safa.features.documents.services.DocumentService;
import edu.nd.crc.safa.features.email.services.EmailService;
import edu.nd.crc.safa.features.errors.repositories.CommitErrorRepository;
import edu.nd.crc.safa.features.flatfiles.services.CheckArtifactNameService;
import edu.nd.crc.safa.features.flatfiles.services.FileDownloadService;
import edu.nd.crc.safa.features.flatfiles.services.FileUploadService;
import edu.nd.crc.safa.features.flatfiles.services.ZipFileService;
import edu.nd.crc.safa.features.generation.api.GenApi;
import edu.nd.crc.safa.features.generation.hgen.HGenService;
import edu.nd.crc.safa.features.generation.search.SearchService;
import edu.nd.crc.safa.features.generation.summary.ProjectSummaryService;
import edu.nd.crc.safa.features.generation.summary.SummaryService;
import edu.nd.crc.safa.features.generation.tgen.services.TraceGenerationService;
import edu.nd.crc.safa.features.github.repositories.GithubAccessCredentialsRepository;
import edu.nd.crc.safa.features.github.repositories.GithubProjectRepository;
import edu.nd.crc.safa.features.github.services.GithubConnectionService;
import edu.nd.crc.safa.features.github.services.GithubGraphQlService;
import edu.nd.crc.safa.features.health.HealthService;
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
import edu.nd.crc.safa.features.memberships.services.MembershipService;
import edu.nd.crc.safa.features.memberships.services.OrganizationMembershipService;
import edu.nd.crc.safa.features.memberships.services.ProjectMembershipService;
import edu.nd.crc.safa.features.memberships.services.TeamMembershipService;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;
import edu.nd.crc.safa.features.organizations.services.TeamService;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
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
import edu.nd.crc.safa.features.users.services.PermissionCheckerService;
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
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.annotation.Scope;
import org.springframework.core.env.Environment;
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
    private final MembershipService membershipService;
    private final TeamMembershipService teamMembershipService;
    private final OrganizationMembershipService orgMembershipService;
    private final ProjectMembershipService projectMembershipService;
    // Orgs
    private final TeamService teamService;
    private final OrganizationService organizationService;
    private final PermissionService permissionService;
    private final PermissionCheckerService permissionCheckerService;
    // Versions
    private final VersionService versionService;
    // Types
    private final TypeService typeService;
    // Artifact
    private final ArtifactRepository artifactRepository;
    private final ArtifactPositionRepository artifactPositionRepository;
    private final ArtifactVersionRepository artifactVersionRepository;
    private final ArtifactService artifactService;
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
    private final JobLoggingService jobLoggingService;
    // Search
    private final SearchService searchService;
    // Summarize
    private final SummaryService summaryService;
    // HGen
    private final HGenService hGenService;
    // Billing
    private final BillingService billingService;
    private final TransactionService transactionService;
    private final CostEstimationService costEstimationService;
    // Config
    private final Environment environment;
    // Jobs
    private JobLauncher jobLauncher; // Not final because runtime changes on test vs dev.
    // Email
    private EmailService emailService;
    // Events
    private ApplicationEventPublisher eventPublisher;
    //chat
    private ChatService chatService;
    private ChatMessageService chatMessageService;
    // Comments
    private CommentService commentService;
    private CommentRetrievalService commentRetrievalService;
    // Health
    private HealthService healthService;

    @PostConstruct
    public void postInit() {
        ServiceProvider.instance = this;
    }

}
