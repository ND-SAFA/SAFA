package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jira.entities.app.JiraIssueDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraProjectResponseDTO;
import edu.nd.crc.safa.features.jira.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.features.jira.entities.db.JiraProject;
import edu.nd.crc.safa.features.jira.repositories.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Setter;
import org.springframework.util.StringUtils;

/**
 * Responsible for providing step implementations for:
 * 1. Connecting to JIRA and accessing project
 * 2. Downloading issues and links in project
 * 3. Saving issues as artifacts
 * 4. Returning project created
 */
public class CreateProjectViaJiraJob extends CommitJob {
    /**
     * The project version to upload entities to.
     */
    protected JiraIdentifier jiraIdentifier;
    /**
     * The credentials used to access the project.
     */
    protected JiraAccessCredentials credentials;
    /**
     * List of issues in project;
     */
    @Setter
    protected List<JiraIssueDTO> issues;
    /**
     * JIRA's response for downloading project
     */
    @Setter
    protected JiraProjectResponseDTO jiraProjectResponse;
    /**
     * The jira project created.
     */
    JiraProject jiraProject;

    private final SafaUser user;

    public CreateProjectViaJiraJob(
        JobDbEntity jobDbEntity,
        ServiceProvider serviceProvider,
        JiraIdentifier jiraIdentifier,
        SafaUser user) {
        super(jobDbEntity, serviceProvider, new ProjectCommit(jiraIdentifier.getProjectVersion(), false));
        this.jiraIdentifier = jiraIdentifier;
        this.issues = new ArrayList<>();
        this.user = user;
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
        JiraAccessCredentialsRepository jiraAccessCredentialsRepository = this.serviceProvider
            .getJiraAccessCredentialsRepository();

        this.credentials = jiraAccessCredentialsRepository
            .findByUser(user)
            .orElseThrow(() -> new SafaError("No JIRA credentials found"));
    }

    @IJobStep(value = "Retrieving Jira Project", position = 2)
    public void retrieveJiraProject() {
        // Step - Get required services
        JiraConnectionService jiraConnectionService = this.serviceProvider.getJiraConnectionService();

        // Step - Retrieve project information including issues
        Long jiraProjectId = this.jiraIdentifier.getJiraProjectId();
        String cloudId = jiraIdentifier.getCloudId();
        this.jiraProjectResponse = jiraConnectionService.retrieveJIRAProject(credentials, cloudId, jiraProjectId);
        this.issues = jiraConnectionService.retrieveJIRAIssues(credentials, cloudId, jiraProjectId).getIssues();
    }

    @IJobStep(value = "Creating SAFA Project", position = 3)
    public void createSafaProject() {
        // Step - Save as SAFA project
        String projectName = this.jiraProjectResponse.getName();
        String projectDescription = this.jiraProjectResponse.getDescription();
        Project project = this.jiraIdentifier.getProjectVersion().getProject();

        // if not already set
        if (!StringUtils.hasLength(project.getName())) {
            project.setName(projectName);
        }
        if (!StringUtils.hasLength(project.getDescription())) {
            project.setDescription(projectDescription);
        }
        this.serviceProvider.getProjectRepository().save(project);

        // Step - Update job name
        this.serviceProvider.getJobService().setJobName(this.getJobDbEntity(), createJobName(projectName));

        // Step - Map JIRA project to SAFA project
        this.jiraProject = this.getJiraProjectMapping(
            project,
            this.jiraIdentifier.getJiraProjectId());
    }

    protected JiraProject getJiraProjectMapping(Project project, Long jiraProjectId)  {
        JiraProject jiraProject = new JiraProject(project, jiraProjectId);

        return this.serviceProvider.getJiraProjectRepository().save(jiraProject);
    }

    @IJobStep(value = "Importing Issues and Links", position = 4)
    public void convertIssuesToArtifactsAndTraceLinks() {
        ProjectEntities projectEntities = this.retrieveJiraEntities();
        this.projectCommit.addArtifacts(ModificationType.ADDED, projectEntities.getArtifacts());
        this.projectCommit.addTraces(ModificationType.ADDED, projectEntities.getTraces());

        jiraProject.setLastUpdate(new Date());
        this.serviceProvider.getJiraProjectRepository().save(jiraProject);
    }

    protected ProjectEntities retrieveJiraEntities() {
        return this.serviceProvider
            .getJiraParsingService()
            .parseProjectEntitiesFromIssues(this.issues);
    }
}
