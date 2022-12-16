package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.util.ArrayList;
import java.util.Base64;
import java.util.Hashtable;
import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.github.entities.app.GithubFileBlobDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryFileDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryFiletreeResponseDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import edu.nd.crc.safa.features.github.repositories.GithubAccessCredentialsRepository;
import edu.nd.crc.safa.features.github.services.GithubConnectionService;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.util.StringUtils;

/**
 * Responsible for providing step implementations for importing a GitHub project:
 * 1. Connecting to GitHub and accessing project
 * 2. Downloading the file tree for the selected branch
 * 3. Saving file paths as artifacts
 * 4. Returning project created
 */
public class GithubProjectCreationJob extends CommitJob {

    /**
     * Internal project identifier
     */
    protected final GithubIdentifier githubIdentifier;

    /**
     * Last commit for the repository we're pulling
     */
    protected String commitSha;

    /**
     * Credentials used to pull GitHub data
     */
    protected GithubAccessCredentials credentials;

    /**
     * Repository pulled data
     */
    protected GithubRepositoryDTO githubRepositoryDTO;

    /**
     * Internal project representation
     */
    protected GithubProject githubProject;

    public GithubProjectCreationJob(JobDbEntity jobDbEntity,
                                    ServiceProvider serviceProvider,
                                    GithubIdentifier githubIdentifier) {
        super(jobDbEntity, serviceProvider, new ProjectCommit(githubIdentifier.getProjectVersion(), false));
        this.githubIdentifier = githubIdentifier;
    }

    public static String createJobName(String repositoryName) {
        return "Importing GitHub project:" + repositoryName;
    }

    public static String createJobName(GithubIdentifier identifier) {
        return createJobName(identifier.getRepositoryName());
    }

    @IJobStep(value = "Authenticating User Credentials", position = 1)
    public void authenticateUserCredentials() {
        GithubAccessCredentialsRepository accessCredentialsRepository = this.serviceProvider
            .getGithubAccessCredentialsRepository();
        SafaUser principal = this.getJobDbEntity().getUser();

        this.credentials = accessCredentialsRepository.findByUser(principal).orElseThrow(() ->
            new SafaError("No GitHub credentials found for user " + principal.getEmail()));
    }

    /**
     * Separate method for retrieving the GitHub project such that it can be mocked
     */
    @IJobStep(value = "Retrieving Github Repository", position = 2)
    public void retrieveGitHubRepository() {
        GithubConnectionService connectionService = serviceProvider.getGithubConnectionService();
        String repositoryName = this.githubIdentifier.getRepositoryName();

        this.githubRepositoryDTO = connectionService.getUserRepository(this.credentials, repositoryName);
    }

    @IJobStep(value = "Creating SAFA Project", position = 3)
    public void createSafaProject() {
        ProjectService projectService = this.serviceProvider.getProjectService();

        // Step - Save as SAFA project
        String projectName = this.githubRepositoryDTO.getName();
        String projectDescription = this.githubRepositoryDTO.getDescription();
        Project project = this.githubIdentifier.getProjectVersion().getProject();

        if (projectDescription == null) {
            projectDescription = projectName;
        }

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

        // Step - Map GitHub project to SAFA project
        this.githubProject = this.getGithubProjectMapping(project);
    }

    protected GithubProject getGithubProjectMapping(Project project) {
        SafaUser principal = this.getJobDbEntity().getUser();
        GithubProject githubProject = new GithubProject();

        githubProject.setProject(project);
        githubProject.setBranch(this.githubRepositoryDTO.getDefaultBranch());
        githubProject.setRepositoryName(this.githubRepositoryDTO.getName());

        return this.serviceProvider.getGithubProjectRepository().save(githubProject);
    }

    @IJobStep(value = "Convert Filetree To Artifacts And TraceLinks", position = 4)
    public void convertFiletreeToArtifactsAndTraceLinks() {
        GithubConnectionService connectionService = serviceProvider.getGithubConnectionService();
        String repositoryName = this.githubIdentifier.getRepositoryName();

        this.commitSha = connectionService.getRepositoryBranch(this.credentials, repositoryName,
            this.githubRepositoryDTO.getDefaultBranch()).getLastCommitSha();
        this.projectCommit.addArtifacts(ModificationType.ADDED, getArtifacts());
        this.githubProject.setLastCommitSha(this.commitSha);
        this.serviceProvider.getGithubProjectRepository().save(githubProject);
    }

    protected List<ArtifactAppEntity> getArtifacts() {
        List<ArtifactAppEntity> artifacts = new ArrayList<>();
        GithubConnectionService connectionService = serviceProvider.getGithubConnectionService();
        GithubRepositoryFiletreeResponseDTO filetreeResponseDTO =
            connectionService.getRepositoryFiles(
                this.credentials,
                this.githubIdentifier.getRepositoryName(),
                this.commitSha);

        for (GithubRepositoryFileDTO file : filetreeResponseDTO.filesOnly().getTree()) {
            GithubFileBlobDTO blobDTO = this.serviceProvider.getGithubConnectionService()
                .getBlobInformation(this.credentials, file.getBlobApiUrl());
            String name = file.getPath();
            String type = file.getType().name();
            String summary = file.getSha();
            String body = "";

            if (blobDTO != null && StringUtils.hasLength(blobDTO.getContent())) {
                body = base64Decode(blobDTO.getContent());
            }

            ArtifactAppEntity artifact = new ArtifactAppEntity(
                null,
                type,
                name,
                summary,
                body,
                DocumentType.ARTIFACT_TREE,
                new Hashtable<>()
            );

            artifacts.add(artifact);
        }

        return artifacts;
    }

    /**
     * Decodes GitHub's base64 encoded file bodies. Each line in the original file
     * is base64 encoded in GitHub's storage, with newlines separating them.
     *
     * @param encodedBody The encoded file body
     * @return The decoded file body
     */
    private String base64Decode(String encodedBody) {
        StringBuilder output = new StringBuilder();

        for (String line : encodedBody.split("\n")) {
            byte[] decodedBytes = Base64.getDecoder().decode(line);
            output.append(new String(decodedBytes));
        }

        return output.toString();
    }
}
