package edu.nd.crc.safa.server.entities.api.jobs;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

import edu.nd.crc.safa.server.accounts.SafaUser;
import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.jira.JiraIssueDTO;
import edu.nd.crc.safa.server.entities.api.jira.JiraProjectResponseDTO;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.jira.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.server.services.ProjectService;
import edu.nd.crc.safa.server.services.ServiceProvider;
import edu.nd.crc.safa.server.services.jira.JiraConnectionService;

import lombok.Setter;

/**
 * Responsible for providing step implementations for:
 * 1. Connecting to JIRA and accessing project
 * 2. Downloading issues and links in project
 * 3. Saving issues as artifacts
 * 4. Returning project created
 */
public class JiraProjectCreationWorker extends ProjectCreationWorker {
    /**
     * The project version to upload entities to.
     */
    ProjectVersion projectVersion;
    /**
     * The JIRA id of the project to scrape.
     */
    Long jiraProjectId;
    /**
     * Id of JIRA resource containing project.
     */
    String cloudId;
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

    public JiraProjectCreationWorker(
        JobDbEntity jobDbEntity,
        ServiceProvider serviceProvider,
        Long jiraProjectId,
        String cloudId) {
        super(jobDbEntity, serviceProvider, new ProjectCommit());
        this.jiraProjectId = jiraProjectId;
        this.cloudId = cloudId;
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
            .findByUserAndCloudId(principal, this.cloudId).orElseThrow(() -> new SafaError("No JIRA credentials "
                + "found"));
    }

    /**
     * Placeholder for retrieving project issues
     */
    public void retrieveJiraProject() {
        // Step - Get required services
        JiraConnectionService jiraConnectionService = this.serviceProvider.getJiraConnectionService();

        // Step - Retrieve project information including issues
        this.jiraProjectResponse = jiraConnectionService.retrieveJIRAProject(credentials,
            jiraProjectId);
        this.issues = jiraConnectionService.retrieveJIRAIssues(credentials, jiraProjectId).getIssues();
    }

    public void createSafaProject() {
        ProjectService projectService = this.serviceProvider.getProjectService();

        // Step - Save as SAFA project
        String projectName = this.jiraProjectResponse.getName();
        String projectDescription = this.jiraProjectResponse.getDescription();
        Project project = new Project(projectName, projectDescription);
        projectService.saveProjectWithCurrentUserAsOwner(project);

        // Step - Update job name
        this.serviceProvider.getJobService().setJobName(this.getJobDbEntity(), createJobName(projectName));

        // Step - Map JIRA project to SAFA project
        this.serviceProvider.getJiraConnectionService().createJiraProjectMapping(project, jiraProjectId);
        this.projectVersion = this.serviceProvider.getProjectService().createInitialProjectVersion(project);
        this.projectCommit.setCommitVersion(this.projectVersion);
    }

    /**
     * Takes all JIRA issues and extracts their name, type, summary, and description
     * to convert them into artifacts. Issue links are also extracted.
     */
    public void convertIssuesToArtifactsAndTraceLinks() {
        List<ArtifactAppEntity> artifacts = new ArrayList<>();
        List<TraceAppEntity> traces = new ArrayList<>();

        for (JiraIssueDTO issue : this.issues) {
            String name = issue.getKey();
            String type = issue.getFields().getIssueType().getName();
            String summary = issue.getFields().getSummary();
            String description = getIssueDescription(issue);

            ArtifactAppEntity artifact = new ArtifactAppEntity(
                "",
                type,
                name,
                summary,
                description,
                DocumentType.ARTIFACT_TREE,
                new Hashtable<>()
            );
            artifacts.add(artifact);
            for (JiraIssueDTO.JiraIssueFields.JiraIssueLink link : issue.getFields().getIssueLinks()) {
                JiraIssueDTO targetArtifact = link.getOutwardIssue();
                if (targetArtifact != null) {
                    String targetName = link.getOutwardIssue().getKey();

                    TraceAppEntity trace = new TraceAppEntity()
                        .asManualTrace()
                        .betweenArtifacts(name, targetName);
                    traces.add(trace);
                }
            }
        }

        this.projectCommit.getArtifacts().getAdded().addAll(artifacts);
        this.projectCommit.getTraces().getAdded().addAll(traces);
    }

    /**
     * Concatenates all issue contents into string delimited by newlines.
     *
     * @param issue The issue whose content is returned.
     * @return String representing delimited content.
     */
    private String getIssueDescription(JiraIssueDTO issue) {
        StringBuilder contentString = new StringBuilder();
        for (JiraIssueDTO.JiraIssueFields.JiraDescription.Content content :
            issue.getFields().getDescription().getContent()) {
            for (JiraIssueDTO.JiraIssueFields.JiraDescription.ContentContent contentContent :
                content.getContent()) {
                contentString.append(contentContent.getText());
            }
        }
        return contentString.toString().strip();
    }
}
