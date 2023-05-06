package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.nio.file.FileSystems;
import java.nio.file.PathMatcher;
import java.util.ArrayList;
import java.util.Base64;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.function.Predicate;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeAppEntity;
import edu.nd.crc.safa.features.attributes.entities.ReservedAttributes;
import edu.nd.crc.safa.features.attributes.services.AttributeService;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.github.entities.api.graphql.Branch;
import edu.nd.crc.safa.features.github.entities.api.graphql.Repository;
import edu.nd.crc.safa.features.github.entities.app.GithubImportDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryFileDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import edu.nd.crc.safa.features.github.repositories.GithubAccessCredentialsRepository;
import edu.nd.crc.safa.features.github.services.GithubGraphQlService;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.ArtifactType;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.graphql.entities.EdgeNode;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.TextNode;

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
    protected Repository githubRepository;

    /**
     * Internal project representation
     */
    protected GithubProject githubProject;

    protected GithubImportDTO importSettings;

    private final SafaUser user;

    private Predicate<String> shouldImportPredicate;

    protected static final int CREATE_PROJECT_STEP_NUM = 3;

    public GithubProjectCreationJob(JobDbEntity jobDbEntity,
                                    ServiceProvider serviceProvider,
                                    GithubIdentifier githubIdentifier,
                                    GithubImportDTO githubImportDTO,
                                    SafaUser user) {
        super(jobDbEntity, serviceProvider);
        this.githubIdentifier = githubIdentifier;
        this.user = user;
        this.importSettings = githubImportDTO;
    }

    public static String createJobName(String repositoryName) {
        return "Importing GitHub project: " + repositoryName;
    }

    public static String createJobName(GithubIdentifier identifier) {
        return createJobName(identifier.getRepositoryName());
    }

    /**
     * Creates a predicate that determines whether a file should be imported. A file should be imported
     * if it matches the include predicate and does not match the exclude predicate. See
     * {@link #globListToPredicate(String)} for how these predicates are created.
     */
    private void createImportPredicate() {
        Predicate<String> includePredicate = globListToPredicate(githubProject.getInclude());
        Predicate<String> excludePredicate = globListToPredicate(githubProject.getExclude());
        shouldImportPredicate = includePredicate.and(excludePredicate.negate());
    }

    /**
     * Creates a matcher predicate from a list of glob patterns. The predicate will return true if
     * the file path matches any of the glob patterns.
     *
     * @param globs List of glob patterns, comma separated
     * @return Predicate that returns true if the file path matches any of the glob patterns
     */
    private Predicate<String> globListToPredicate(String globs) {
        List<String> globList = List.of(globs.split(","));
        return globList.stream()                            // For each glob pattern from the front end:
            .map(pattern -> "glob:" + pattern)              //   Prepend "glob:" (needed for path matcher)
            .map(FileSystems.getDefault()::getPathMatcher)  //   Create a path matcher
            .map(this::matcherToPredicate)                  //   Convert to a predicate
            .reduce(Predicate::or)                          //   Or the predicates together (if any match, return true)
            .orElse(path -> false);                         // If no glob patterns, return false
    }

    /**
     * Converts a path matcher to a predicate
     *
     * @param matcher Path matcher
     * @return Predicate that returns true if the file path matches the path matcher
     */
    private Predicate<String> matcherToPredicate(PathMatcher matcher) {
        return string -> matcher.matches(FileSystems.getDefault().getPath(string));
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
     *
     * @param logger Logger for this job
     */
    @IJobStep(value = "Retrieving Github Repository", position = 2)
    public void retrieveGitHubRepository(JobLogger logger) {
        GithubGraphQlService ghService = serviceProvider.getGithubGraphQlService();
        String repositoryName = this.githubIdentifier.getRepositoryName();
        String owner = this.githubIdentifier.getRepositoryOwner();

        this.githubRepository = ghService.getGithubRepository(user, owner, repositoryName).getData().getRepository();

        logger.log("GitHub repository '%s' retrieved.", githubRepository.getName());
    }

    @IJobStep(value = "Creating SAFA Project", position = CREATE_PROJECT_STEP_NUM)
    public void createSafaProject(JobLogger logger) {
        // Step - Save as SAFA project
        String projectName = this.githubRepository.getName();
        String projectDescription = this.githubRepository.getDescription();

        if (projectDescription == null) {
            projectDescription = projectName;
        }

        ProjectVersion projectVersion = createProject(user, projectName, projectDescription);
        this.githubIdentifier.setProjectVersion(projectVersion);

        Project project = projectVersion.getProject();
        logger.log("Created new project '%s' with id %s", project.getName(), project.getProjectId());
    }

    @IJobStep(value = "Creating SAFA Project -> Github Repository Mapping", position = 4)
    public void createSafaProjectMapping(JobLogger logger) {
        String projectName = this.githubRepository.getName();
        Project project = this.githubIdentifier.getProjectVersion().getProject();

        // Step - Update job name
        this.serviceProvider.getJobService().setJobName(this.getJobDbEntity(), createJobName(projectName));

        createCustomAttributes(project);

        // Step - Map GitHub project to SAFA project
        this.githubProject = this.getGithubProjectMapping(project);
        createImportPredicate();

        logger.log("Project %s is mapped to GitHub project %s.", project.getProjectId(), githubProject.getId());
    }

    /**
     * Creates custom attributes that are used for the github import.
     *
     * @param project The project we're importing into
     */
    private void createCustomAttributes(Project project) {
        for (CustomAttributeAppEntity attribute : ReservedAttributes.Github.ALL_ATTRIBUTES) {
            AttributeService attributeService = serviceProvider.getAttributeService();

            if (attributeService.getByProjectAndKeyname(project, attribute.getKey()).isEmpty()) {
                serviceProvider.getAttributeService().saveEntity(attribute, project, true);
            }
        }
    }

    /**
     * Creates a github project mapping for this project based on the job settings.
     *
     * @param project The project we're importing into.
     * @return The github project mapping.
     */
    protected GithubProject getGithubProjectMapping(Project project) {
        GithubProject githubProject = new GithubProject();

        githubProject.setProject(project);
        githubProject.setOwner(this.githubRepository.getOwner().getLogin());
        githubProject.setRepositoryName(this.githubRepository.getName());

        applyImportSettings(project, githubProject);

        return this.serviceProvider.getGithubProjectRepository().save(githubProject);
    }

    /**
     * Applies the import settings to the github project definition, updating values if they are present
     * in the import settings.
     *
     * @param project The project we're importing into.
     * @param ghProject The github project mapping.
     */
    protected void applyImportSettings(Project project, GithubProject ghProject) {
        ghProject.setArtifactType(getArtifactTypeMapping(project));

        if (importSettings.getInclude() != null) {
            ghProject.setInclude(String.join(",", importSettings.getInclude()));
        }

        if (importSettings.getExclude() != null) {
            ghProject.setExclude(String.join(",", importSettings.getExclude()));
        }

        if (importSettings.getBranch() != null) {
            ghProject.setBranch(importSettings.getBranch());
        } else {
            ghProject.setBranch(this.githubRepository.getDefaultBranchRef().getName());
        }
    }

    /**
     * Gets the artifact type mapping for this import based on the job settings. If the
     * type id is null, it will default to {@code "GitHub File"}. If the type does not exist,
     * it will be created.
     *
     * @param project The project we're importing into.
     * @return The artifact type we should use for importing.
     */
    protected ArtifactType getArtifactTypeMapping(Project project) {
        String artifactTypeId = this.importSettings.getArtifactType();
        artifactTypeId = artifactTypeId != null ? artifactTypeId : getDefaultTypeName();

        ArtifactType artifactType = serviceProvider.getTypeService().getArtifactType(project, artifactTypeId);

        if (artifactType == null) {
            artifactType = serviceProvider.getTypeService().createArtifactType(project, artifactTypeId);

        }

        return artifactType;
    }

    /**
     * Gets the default artifact type name for this import.
     *
     * @return The default artifact type name.
     */
    protected String getDefaultTypeName() {
        return "GitHub File";
    }

    @IJobStep(value = "Convert Filetree To Artifacts And TraceLinks", position = 5)
    public void convertFiletreeToArtifactsAndTraceLinks(JobLogger logger) {
        ProjectCommit commit = getProjectCommit();
        Branch branch = getBranch(this.githubProject.getBranch());
        this.commitSha = branch.getTarget().getOid();
        commit.addArtifacts(ModificationType.ADDED, getArtifacts());
        this.githubProject.setLastCommitSha(this.commitSha);
        this.serviceProvider.getGithubProjectRepository().save(githubProject);

        logger.log("Retrieved %d artifacts from project.", commit.getArtifacts().getSize());
    }

    /**
     * Get the branch definition with the given name.
     *
     * @param targetBranch The name of the branch.
     * @return The branch if it exists, otherwise the default branch.
     */
    protected Branch getBranch(String targetBranch) {
        return this.githubRepository.getRefs().getEdges().stream()
            .map(EdgeNode::getNode)
            .filter(branch -> branch.getName().equals(targetBranch))
            .findFirst()
            .orElse(this.githubRepository.getDefaultBranchRef());
    }

    protected List<ArtifactAppEntity> getArtifacts() {
        List<ArtifactAppEntity> artifacts = new ArrayList<>();
        GithubGraphQlService githubService = serviceProvider.getGithubGraphQlService();
        List<GithubRepositoryFileDTO> files = githubService.getFilesInRepo(this.user,
            this.githubIdentifier.getRepositoryOwner(),
            this.githubIdentifier.getRepositoryName(),
            this.githubProject.getBranch());

        for (GithubRepositoryFileDTO file : files) {

            String path = file.getPath();
            if (shouldSkipFile(path)) {
                continue;
            }

            String type = githubProject.getArtifactType().getName();
            String summary = "";  // TODO I don't think this field is shown to the user at all
            String body = Objects.requireNonNullElse(file.getContents(), "null");

            Map<String, JsonNode> attributes = new HashMap<>();
            attributes.put(ReservedAttributes.Github.REPO_PATH.getKey(), TextNode.valueOf(file.getPath()));
            attributes.put(ReservedAttributes.Github.LINK.getKey(),
                TextNode.valueOf(buildGithubFileUrl(file.getPath())));

            ArtifactAppEntity artifact = new ArtifactAppEntity(
                null,
                type,
                file.getName(),
                summary,
                body,
                DocumentType.ARTIFACT_TREE,
                attributes
            );

            artifacts.add(artifact);
        }

        return artifacts;
    }

    private String buildGithubFileUrl(String filePath) {
        return String.join("/",
            "https://github.com",
            githubProject.getOwner(),
            githubProject.getRepositoryName(),
            "blob",
            githubProject.getBranch(),
            filePath);
    }

    /**
     * Determines if the given filename should be imported based on the include/exclude settings.
     * If the include list is empty, no files are included. If the exclude list is empty, no files are excluded.
     *
     * @param filename The filename to check.
     * @return True if the file should be imported, otherwise false.
     */
    protected boolean shouldSkipFile(String filename) {
        return !shouldImportPredicate.test(filename);
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
