package edu.nd.crc.safa.server.entities.api.jobs;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.jobs.entities.app.ProjectCreationJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.api.github.GithubFileBlobDTO;
import edu.nd.crc.safa.server.entities.api.github.GithubRepositoryDTO;
import edu.nd.crc.safa.server.entities.api.github.GithubRepositoryFileDTO;
import edu.nd.crc.safa.server.entities.api.github.GithubRepositoryFiletreeResponseDTO;
import edu.nd.crc.safa.server.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.server.entities.db.GithubProject;
import edu.nd.crc.safa.server.repositories.github.GithubAccessCredentialsRepository;
import edu.nd.crc.safa.server.services.github.GithubConnectionService;

/**
 * Responsible for providing step implementations for importing a GitHub project:
 * 1. Connecting to GitHub and accessing project
 * 2. Downloading the file tree for the selected branch
 * 3. Saving file paths as artifacts
 * 4. Returning project created
 */
public class GithubProjectCreationJob extends ProjectCreationJob {

    private final String repositoryName;

    private String commitSha;

    private GithubAccessCredentials credentials;

    private GithubRepositoryDTO githubRepositoryDTO;

    private GithubRepositoryFiletreeResponseDTO filetreeResponseDTO;

    private ProjectVersion projectVersion;

    public GithubProjectCreationJob(JobDbEntity jobDbEntity,
                                    ServiceProvider serviceProvider,
                                    String repositoryName) {
        super(jobDbEntity, serviceProvider, new ProjectCommit());
        this.repositoryName = repositoryName;
    }

    public static String createJobName(String repositoryName) {
        return "Importing GitHub project:" + repositoryName;
    }

    public void authenticateUserCredentials() {
        SafaUserService safaUserService = this.serviceProvider.getSafaUserService();
        GithubAccessCredentialsRepository accessCredentialsRepository = this.serviceProvider
            .getGithubAccessCredentialsRepository();
        SafaUser principal = safaUserService.getCurrentUser();

        this.credentials = accessCredentialsRepository.findByUser(principal).orElseThrow(() ->
            new SafaError("No GitHub credentials found for user " + principal.getEmail()));
    }

    /**
     * Separate method for retrieving the GitHub project such that it can be mocked
     */
    public void retrieveGitHubRepository() {
        GithubConnectionService connectionService = serviceProvider.getGithubConnectionService();

        this.githubRepositoryDTO = connectionService.getUserRepository(this.credentials, this.repositoryName);
        this.commitSha = connectionService.getRepositoryBranch(this.credentials, this.repositoryName,
            this.githubRepositoryDTO.getDefaultBranch()).getLastCommitSha();
        this.filetreeResponseDTO = connectionService.getRepositoryFiles(this.credentials, this.repositoryName,
            this.commitSha);
    }

    public void createSafaProject() {
        ProjectService projectService = this.serviceProvider.getProjectService();

        // Step - Save as SAFA project
        String projectName = this.githubRepositoryDTO.getName();
        String projectDescription = this.githubRepositoryDTO.getDescription();
        Project project = new Project(projectName, projectDescription);

        projectService.saveProjectWithCurrentUserAsOwner(project);

        // Step - Update job name
        this.serviceProvider.getJobService().setJobName(this.getJobDbEntity(), createJobName(projectName));

        // Step - Map GitHub project to SAFA project
        this.createGithubProjectMapping(project);
        this.projectVersion = this.serviceProvider.getProjectService().createInitialProjectVersion(project);
        this.projectCommit.setCommitVersion(this.projectVersion);
    }

    private void createGithubProjectMapping(Project project) {
        SafaUserService safaUserService = this.serviceProvider.getSafaUserService();
        SafaUser principal = safaUserService.getCurrentUser();
        GithubProject githubProject = new GithubProject();

        githubProject.setProject(project);
        githubProject.setBranch(this.githubRepositoryDTO.getDefaultBranch());
        githubProject.setRepositoryName(this.githubRepositoryDTO.getName());
        githubProject.setLastCommitSha(this.commitSha);
        githubProject.setUser(principal);
        this.serviceProvider.getGithubProjectRepository().save(githubProject);
    }

    public void convertFiletreeToArtifactsAndTraceLinks() {
        List<ArtifactAppEntity> artifacts = new ArrayList<>();

        for (GithubRepositoryFileDTO file : this.filetreeResponseDTO.filterOutFolders().getTree()) {
            GithubFileBlobDTO blobDTO = this.serviceProvider.getGithubConnectionService()
                .getBlobInformation(this.credentials, file.getBlobApiUrl());
            String name = file.getPath();
            String type = file.getType().name();
            String summary = file.getSha();
            String body = blobDTO.getContent();

            ArtifactAppEntity artifact = new ArtifactAppEntity(
                "",
                type,
                name,
                summary,
                body,
                DocumentType.ARTIFACT_TREE,
                new Hashtable<>()
            );

            artifacts.add(artifact);
        }

        this.projectCommit.addArtifacts(ModificationType.ADDED, artifacts);
    }
}
