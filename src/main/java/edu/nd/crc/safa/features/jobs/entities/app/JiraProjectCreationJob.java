package edu.nd.crc.safa.features.jobs.entities.app;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.flatfiles.entities.common.ProjectEntities;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jira.entities.app.JiraIssueDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraProjectResponseDTO;
import edu.nd.crc.safa.features.jira.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.features.jira.repositories.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;

import lombok.Setter;

/**
 * Responsible for providing step implementations for:
 * 1. Connecting to JIRA and accessing project
 * 2. Downloading issues and links in project
 * 3. Saving issues as artifacts
 * 4. Returning project created
 */
public class JiraProjectCreationJob extends ProjectCreationJob {
    /**
     * The project version to upload entities to.
     */
    JiraIdentifier jiraIdentifier;
    /**
     * The credentials used to access the project.
     */
    JiraAccessCredentials credentials;
    /**
     * List of issues in project;
     */
    @Setter
    List<JiraIssueDTO> issues;
    /**
     * JIRA's response for downloading project
     */
    @Setter
    JiraProjectResponseDTO jiraProjectResponse;

    public JiraProjectCreationJob(
        JobDbEntity jobDbEntity,
        ServiceProvider serviceProvider,
        JiraIdentifier jiraIdentifier) {
        super(jobDbEntity, serviceProvider, new ProjectCommit(jiraIdentifier.getProjectVersion(), false));
        this.jiraIdentifier = jiraIdentifier;
        this.issues = new ArrayList<>();
    }

    public static String createJobName(String jiraProjectName) {
        return "Importing JIRA project:" + jiraProjectName;
    }

    public void authenticateUserCredentials() {
        // Step - Get services needed
        SafaUserService safaUserService = this.serviceProvider.getSafaUserService();
        JiraAccessCredentialsRepository jiraAccessCredentialsRepository = this.serviceProvider
            .getJiraAccessCredentialsRepository();

        SafaUser principal = safaUserService.getCurrentUser();
        this.credentials = jiraAccessCredentialsRepository
            .findByUserAndCloudId(principal, this.jiraIdentifier.getCloudId()).orElseThrow(() -> new SafaError("No "
                + "JIRA credentials "
                + "found"));
    }

    /**
     * Placeholder for retrieving project issues
     */
    public void retrieveJiraProject() {
        // Step - Get required services
        JiraConnectionService jiraConnectionService = this.serviceProvider.getJiraConnectionService();

        // Step - Retrieve project information including issues
        Long jiraProjectId = this.jiraIdentifier.getJiraProjectId();
        this.jiraProjectResponse = jiraConnectionService.retrieveJIRAProject(credentials,
            jiraProjectId);
        this.issues = jiraConnectionService.retrieveJIRAIssues(credentials, jiraProjectId).getIssues();
    }

    public void createSafaProject() {
        // Step - Save as SAFA project
        String projectName = this.jiraProjectResponse.getName();
        String projectDescription = this.jiraProjectResponse.getDescription();
        Project project = this.jiraIdentifier.getProjectVersion().getProject();
        project.setName(projectName);
        project.setDescription(projectDescription);
        this.serviceProvider.getProjectRepository().save(project);

        // Step - Update job name
        this.serviceProvider.getJobService().setJobName(this.getJobDbEntity(), createJobName(projectName));

        // Step - Map JIRA project to SAFA project
        this.serviceProvider.getJiraConnectionService().createJiraProjectMapping(project,
            this.jiraIdentifier.getJiraProjectId());
    }

    /**
     * Takes all JIRA issues and extracts their name, type, summary, and description
     * to convert them into artifacts. Issue links are also extracted.
     */
    public void convertIssuesToArtifactsAndTraceLinks() {
        ProjectEntities projectEntities =
            this.serviceProvider.getJiraParsingService().parseProjectEntitiesFromIssues(this.issues);
        this.projectCommit.addArtifacts(ModificationType.ADDED, projectEntities.getArtifacts());
        this.projectCommit.addTraces(ModificationType.ADDED, projectEntities.getTraces());
    }
}
