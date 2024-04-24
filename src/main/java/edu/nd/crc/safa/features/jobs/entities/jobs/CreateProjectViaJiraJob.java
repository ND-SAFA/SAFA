package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jira.entities.api.JiraImportSettings;
import edu.nd.crc.safa.features.jira.entities.app.JiraIssueDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraProjectResponseDTO;
import edu.nd.crc.safa.features.jira.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.features.jira.entities.db.JiraProject;
import edu.nd.crc.safa.features.jira.repositories.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectOwner;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.Setter;

/**
 * Responsible for providing step implementations for:
 * 1. Connecting to JIRA and accessing project
 * 2. Downloading issues and links in project
 * 3. Saving issues as artifacts
 * 4. Returning project created
 */
public class CreateProjectViaJiraJob extends CommitJob {
    protected static final int CREATE_PROJECT_STEP_INDEX = 3;
    private final SafaUser user;
    /**
     * The project version to upload entities to.
     */
    @Getter(AccessLevel.PROTECTED)
    private final JiraIdentifier jiraIdentifier;
    /**
     * The credentials used to access the project.
     */
    @Getter(AccessLevel.PROTECTED)
    private JiraAccessCredentials credentials;
    /**
     * List of issues in project;
     */
    @Setter
    private List<JiraIssueDTO> issues;
    /**
     * JIRA's response for downloading project
     */
    @Setter
    private JiraProjectResponseDTO jiraProjectResponse;
    /**
     * The jira project created.
     */
    @Getter(AccessLevel.PROTECTED)
    private JiraProject jiraProject;

    @Getter(AccessLevel.PROTECTED)
    private final JiraImportSettings importSettings;

    public CreateProjectViaJiraJob(JobDbEntity jobDbEntity, ServiceProvider serviceProvider,
                                   JiraIdentifier jiraIdentifier, SafaUser user, JiraImportSettings importSettings) {
        super(user, jobDbEntity, serviceProvider, new ProjectCommitDefinition(), true);
        this.jiraIdentifier = jiraIdentifier;
        this.issues = new ArrayList<>();
        this.user = user;
        this.importSettings = importSettings;
    }

    public static String createJobName(JiraIdentifier jiraIdentifier) {
        return createJobName(jiraIdentifier.getJiraProjectId().toString());
    }

    public static String createJobName(String jiraProjectName) {
        return "Importing JIRA project: " + jiraProjectName;
    }

    @IJobStep(value = "Authenticating User Credentials", position = 1)
    public void authenticateUserCredentials() {
        // Step - Get services needed
        JiraAccessCredentialsRepository jiraAccessCredentialsRepository = this.getServiceProvider()
            .getJiraAccessCredentialsRepository();

        this.credentials = jiraAccessCredentialsRepository
            .findByUser(user)
            .orElseThrow(() -> new SafaError("No JIRA credentials found"));
    }

    @IJobStep(value = "Retrieving Jira Project", position = 2)
    public void retrieveJiraProject(JobLogger logger) {
        // Step - Get required services
        JiraConnectionService jiraConnectionService = this.getServiceProvider().getJiraConnectionService();

        // Step - Retrieve project information including issues
        Long jiraProjectId = this.jiraIdentifier.getJiraProjectId();
        UUID orgId = jiraIdentifier.getOrgId();
        this.jiraProjectResponse = jiraConnectionService.retrieveJIRAProject(credentials, orgId, jiraProjectId);
        this.issues = jiraConnectionService.retrieveJIRAIssues(credentials, orgId, jiraProjectId);

        logger.log("Jira project '%s' successfully retrieved. %d issues will be imported",
            jiraProjectResponse.getName(), issues.size());
    }

    @IJobStep(value = "Creating SAFA Project", position = CREATE_PROJECT_STEP_INDEX)
    public void createSafaProject(JobLogger logger) {
        // Step - Save as SAFA project
        String projectName = this.jiraProjectResponse.getName();
        String projectDescription = this.jiraProjectResponse.getDescription();

        ProjectOwner owner =
            ProjectOwner.fromUUIDs(getServiceProvider(), importSettings.getTeamId(),
                importSettings.getOrgId(), getUser());
        createProjectAndCommit(owner, projectName, projectDescription);
        ProjectVersion projectVersion = getProjectVersion();
        linkProjectToJob(projectVersion.getProject());

        Project project = projectVersion.getProject();
        this.jiraIdentifier.setProjectVersion(projectVersion);

        logger.log("Created new project '%s' with id %s", project.getName(), project.getProjectId());

        // Step - Update job name
        this.getServiceProvider().getJobService().setJobName(this.getJobDbEntity(), createJobName(projectName));
    }

    @IJobStep(value = "Creating SAFA Project to Jira Project Mapping", position = 4)
    public void mapSafaProject(JobLogger logger) {
        Project project = getProjectCommitDefinition().getCommitVersion().getProject();

        // Step - Map JIRA project to SAFA project
        this.jiraProject = this.getJiraProjectMapping(
            project,
            this.jiraIdentifier.getOrgId(),
            this.jiraIdentifier.getJiraProjectId());

        logger.log("Project %s is mapped to Jira project %s within org with ID %s.", project.getProjectId(),
            jiraProject.getJiraProjectId(), jiraProject.getOrgId());
    }

    protected JiraProject getJiraProjectMapping(Project project, UUID orgId, Long jiraProjectId) {
        JiraProject jiraProject = new JiraProject(project, orgId, jiraProjectId);

        return this.getServiceProvider().getJiraProjectRepository().save(jiraProject);
    }

    @IJobStep(value = "Importing Issues and Links", position = 5)
    public void convertIssuesToArtifactsAndTraceLinks() {
        ProjectEntities projectEntities = this.retrieveJiraEntities();
        getProjectCommitDefinition().addArtifacts(ModificationType.ADDED, projectEntities.getArtifacts());
        getProjectCommitDefinition().addTraces(ModificationType.ADDED, projectEntities.getTraces());

        jiraProject.setLastUpdate(new Date());
        this.getServiceProvider().getJiraProjectRepository().save(jiraProject);
    }

    protected ProjectEntities retrieveJiraEntities() {
        return this.getServiceProvider()
            .getJiraParsingService()
            .parseProjectEntitiesFromIssues(this.issues);
    }
}
