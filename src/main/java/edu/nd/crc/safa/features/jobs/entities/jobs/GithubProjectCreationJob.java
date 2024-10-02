package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.nio.file.FileSystems;
import java.nio.file.PathMatcher;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.function.Predicate;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.attributes.entities.AttributeLayoutAppEntity;
import edu.nd.crc.safa.features.attributes.entities.AttributePositionAppEntity;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeAppEntity;
import edu.nd.crc.safa.features.attributes.entities.ReservedAttributes;
import edu.nd.crc.safa.features.attributes.services.AttributeService;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.email.services.EmailService;
import edu.nd.crc.safa.features.github.entities.api.GithubGraphQlTreeObjectsResponse;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.github.entities.api.graphql.Branch;
import edu.nd.crc.safa.features.github.entities.api.graphql.Repository;
import edu.nd.crc.safa.features.github.entities.app.GithubImportDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryFileDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryFileType;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import edu.nd.crc.safa.features.github.entities.events.GithubProjectImportedEvent;
import edu.nd.crc.safa.features.github.entities.events.ProjectSummarizedEvent;
import edu.nd.crc.safa.features.github.repositories.GithubAccessCredentialsRepository;
import edu.nd.crc.safa.features.github.services.GithubGraphQlService;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.types.services.TypeService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectOwner;
import edu.nd.crc.safa.utilities.exception.ExternalAPIException;
import edu.nd.crc.safa.utilities.graphql.entities.EdgeNode;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.TextNode;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.Setter;
import org.springframework.context.ApplicationEventPublisher;

/**
 * Responsible for providing step implementations for importing a GitHub project:
 * 1. Connecting to GitHub and accessing project
 * 2. Downloading the file tree for the selected branch
 * 3. Saving file paths as artifacts
 * 4. Returning project created
 */
public class GithubProjectCreationJob extends CommitJob {

    protected static final int CREATE_PROJECT_STEP_NUM = 3;
    private static final String GLOB_SEPARATOR = "\0";
    private final String[] DEFAULT_BRANCHES = {
        "master",
        "main",
        "dev",
        "development",
        "prod",
        "production"
    };
    /**
     * Internal project identifier
     */
    @Getter(AccessLevel.PROTECTED)
    private final GithubIdentifier githubIdentifier;
    private final SafaUser user;
    private final GithubImportDTO importSettings;
    /**
     * Last commit for the repository we're pulling
     */
    private String commitSha;
    /**
     * Credentials used to pull GitHub data
     */
    @Getter(AccessLevel.PROTECTED)
    private GithubAccessCredentials credentials;
    /**
     * Repository pulled data
     */
    private Repository githubRepository;
    /**
     * Internal project representation
     */
    @Getter(AccessLevel.PROTECTED)
    @Setter(AccessLevel.PROTECTED)
    private GithubProject githubProject;
    private Predicate<String> shouldImportPredicate;

    public GithubProjectCreationJob(SafaUser user,
                                    JobDbEntity jobDbEntity,
                                    ServiceProvider serviceProvider,
                                    GithubIdentifier githubIdentifier,
                                    GithubImportDTO githubImportDTO) {
        super(user, jobDbEntity, serviceProvider, new ProjectCommitDefinition(), true);
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
        List<String> globList = List.of(globs.split(GLOB_SEPARATOR));
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
        GithubAccessCredentialsRepository accessCredentialsRepository = this.getServiceProvider()
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
        GithubGraphQlService ghService = getServiceProvider().getGithubGraphQlService();
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
        ProjectOwner owner =
            ProjectOwner.fromUUIDs(getServiceProvider(), importSettings.getTeamId(),
                importSettings.getOrgId(), getUser());
        createProjectAndCommit(owner, projectName, projectDescription);
        ProjectVersion projectVersion = getProjectVersion();
        this.githubIdentifier.setProjectVersion(projectVersion);
        linkProjectToJob(projectVersion.getProject());

        Project project = projectVersion.getProject();
        logger.log("Created new project '%s' with id %s", project.getName(), project.getProjectId());
    }

    @IJobStep(value = "Creating SAFA Project -> Github Repository Mapping", position = 4)
    public void createSafaProjectMapping(JobLogger logger) {
        String projectName = this.githubRepository.getName();
        Project project = this.githubIdentifier.getProjectVersion().getProject();

        // Step - Update job name
        this.getServiceProvider().getJobService().setJobName(this.getJobDbEntity(), createJobName(projectName));

        createCustomAttributes(this.user, project);

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
    private void createCustomAttributes(SafaUser user, Project project) {
        for (CustomAttributeAppEntity attribute : ReservedAttributes.Github.ALL_ATTRIBUTES) {
            AttributeService attributeService = getServiceProvider().getAttributeService();

            if (attributeService.getByProjectAndKeyname(project, attribute.getKey()).isEmpty()) {
                getServiceProvider().getAttributeService().saveEntity(user, project, attribute, true);
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

        return this.getServiceProvider().getGithubProjectRepository().save(githubProject);
    }

    /**
     * Applies the import settings to the github project definition, updating values if they are present
     * in the import settings.
     *
     * @param project   The project we're importing into.
     * @param ghProject The github project mapping.
     */
    protected void applyImportSettings(Project project, GithubProject ghProject) {
        ghProject.setArtifactType(getArtifactTypeMapping(project));

        if (importSettings.getInclude() != null) {
            ghProject.setInclude(String.join(GLOB_SEPARATOR, importSettings.getInclude()));
        }

        if (importSettings.getExclude() != null) {
            ghProject.setExclude(String.join(GLOB_SEPARATOR, importSettings.getExclude()));
        }

        if (importSettings.getBranch() != null) {
            ghProject.setBranch(importSettings.getBranch());
        } else {
            ghProject.setBranch(getDefaultBranch(this.githubRepository));
        }
    }

    /**
     * Get the default branch for a repository
     *
     * @param githubRepository The repository
     * @return The default branch if we could determine one, or null otherwise
     */
    private String getDefaultBranch(Repository githubRepository) {
        // If there is a default branch use that
        if (githubRepository.getDefaultBranchRef() != null) {
            return githubRepository.getDefaultBranchRef().getName();
        }

        // If there is only one branch use that
        if (githubRepository.getRefs().getEdges().size() == 1) {
            return githubRepository.getRefs().getEdges().get(0).getNode().getName();
        }

        Map<String, String> branches = new HashMap<>(githubRepository.getRefs().getEdges().size());
        githubRepository.getRefs().getEdges().stream()
            .map(EdgeNode::getNode)
            .map(Branch::getName)
            .forEach(branchName -> branches.put(branchName.toLowerCase(), branchName));

        // Check if they have any branches we recognize as possible defaults
        for (String possibleBranchName : DEFAULT_BRANCHES) {
            if (branches.containsKey(possibleBranchName)) {
                return branches.get(possibleBranchName);
            }
        }

        // Give up - if there are multiple branches still we don't have a good criteria to pick
        return null;
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
        TypeService typeService = getServiceProvider().getTypeService();
        String artifactTypeName = this.importSettings.getArtifactType();
        artifactTypeName = artifactTypeName != null ? artifactTypeName : getDefaultTypeName();

        ArtifactType artifactType = typeService.getArtifactType(project, artifactTypeName);

        if (artifactType == null) {
            artifactType = createArtifactType(project, artifactTypeName);

        }

        return artifactType;
    }

    private ArtifactType createArtifactType(Project project, String artifactTypeName) {
        ArtifactType artifactType = getServiceProvider().getTypeService()
            .createArtifactType(project, artifactTypeName, user);
        List<AttributePositionAppEntity> attributePositions = List.of(
            new AttributePositionAppEntity(ReservedAttributes.Github.LINK.getKey(), 0, 0, 1, 1)
        );
        AttributeLayoutAppEntity layoutEntity = new AttributeLayoutAppEntity(null, artifactTypeName + " Layout",
            List.of(artifactTypeName), attributePositions);
        getServiceProvider().getAttributeLayoutService().saveLayoutEntity(user, layoutEntity, project, true);
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
        ProjectCommitDefinition commit = getProjectCommitDefinition();

        logger.log("Attempting to find branch \"%s\".", this.githubProject.getBranch());
        Branch branch = getBranch(this.githubProject.getBranch());

        this.commitSha = branch.getTarget().getOid();
        commit.addArtifacts(ModificationType.ADDED, getArtifacts(logger));
        this.githubProject.setLastCommitSha(this.commitSha);
        this.getServiceProvider().getGithubProjectRepository().save(githubProject);

        logger.log("Retrieved %d artifacts from project.", commit.getArtifacts().getSize());
    }

    @IJobStep(value = "Generate Summaries", position = 6)
    public void generateSummaries(JobLogger logger) {
        if (!importSettings.isSummarize()) {
            return;
        }

        List<ArtifactAppEntity> newArtifacts = getProjectCommitDefinition().getArtifactList(ModificationType.ADDED);
        getServiceProvider().getProjectSummaryService().summarizeProjectEntities(
            this.user,
            this.getProjectVersion(),
            newArtifacts,
            logger,
            true
        );

        // The summarization above commits the artifacts, so there's no need for the job to do it again later
        newArtifacts.clear();
    }

    @Override
    protected void afterJob(boolean success) {
        if (success) {
            ApplicationEventPublisher eventPublisher = getServiceProvider().getEventPublisher();
            Project project = getProjectVersion().getProject();

            eventPublisher.publishEvent(new GithubProjectImportedEvent(this, user, project, githubIdentifier));
            if (importSettings.isSummarize()) {
                eventPublisher.publishEvent(new ProjectSummarizedEvent(this, user, project));
            }
        }

        if (importSettings.isSummarize()) {
            EmailService emailService = getServiceProvider().getEmailService();
            emailService.sendGenerationFinished(getUser().getEmail(), getProjectVersion(), getJobDbEntity(), success);
        }
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
            .orElseThrow(() -> new SafaError("Either no branch was supplied and no suitable default could be "
                + "determined or the supplied branch could not be found."));
    }

    protected List<ArtifactAppEntity> getArtifacts(JobLogger logger) {
        List<ArtifactAppEntity> artifacts = new ArrayList<>();
        GithubGraphQlService githubGraphQlService = getServiceProvider().getGithubGraphQlService();

        String branch = githubProject.getBranch() + ":";
        String owner = githubIdentifier.getRepositoryOwner();
        String name = githubIdentifier.getRepositoryName();
        Queue<String> locations = new LinkedList<>();
        locations.add(branch);

        while (!locations.isEmpty()) {
            String currentLocation = locations.poll();

            GithubGraphQlTreeObjectsResponse response;
            StringBuilder locationLogBuilder = new StringBuilder();
            try {
                locationLogBuilder.append("## Retrieving files from *").append(currentLocation).append("*\n\n");
                response = githubGraphQlService.getGithubTreeObjects(user, owner, name, currentLocation);
                List<GithubRepositoryFileDTO> locationFiles =
                    GithubRepositoryFileDTO.fromGithubGraphQlResponse(response);

                for (GithubRepositoryFileDTO file : locationFiles) {
                    if (file.getType() == GithubRepositoryFileType.FILE) {
                        processFile(file, artifacts, locationLogBuilder);
                    } else if (file.getType() == GithubRepositoryFileType.FOLDER) {
                        locations.add(branch + file.getPath());
                    } else if (file.getType() == GithubRepositoryFileType.SUBMODULE) {
                        locationLogBuilder.append("**WARNING**: Submodule found at `")
                            .append(file.getPath())
                            .append("` but submodules are not supported\n\n");
                    }
                }
            } catch (ExternalAPIException | NullPointerException e) {
                locationLogBuilder.append("**ERROR**: Failed to retrieve files: `")
                    .append(e.getMessage()).append("`\n\n");
            } finally {
                logger.log(locationLogBuilder.toString());
            }
        }

        return artifacts;
    }

    private void processFile(GithubRepositoryFileDTO file, List<ArtifactAppEntity> artifacts, StringBuilder logger) {
        String path = file.getPath();
        if (shouldSkipFile(path)) {
            logger.append('`').append(path).append("` will not be imported due to inclusion/exclusion criteria.\n\n");
            return;
        }
        logger.append("Importing *").append(path).append("*\n\n");

        String type = githubProject.getArtifactType().getName();
        String summary = "";
        String body = file.isBinary() ? "<binary file>" : file.getContents();

        Map<String, JsonNode> attributes = getAttributes(file.getPath());

        ArtifactAppEntity artifact = new ArtifactAppEntity(
            null,
            type,
            path,
            summary,
            body,
            attributes
        );

        artifacts.add(artifact);
    }

    protected Map<String, JsonNode> getAttributes(String filePath) {
        Map<String, JsonNode> attributes = new HashMap<>();
        attributes.put(ReservedAttributes.Github.LINK.getKey(),
            TextNode.valueOf(buildGithubFileUrl(filePath)));
        return attributes;
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

}
