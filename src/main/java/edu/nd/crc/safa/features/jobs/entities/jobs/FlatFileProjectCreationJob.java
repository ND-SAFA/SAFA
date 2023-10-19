package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.EntityParsingResult;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.errors.repositories.CommitErrorRepository;
import edu.nd.crc.safa.features.flatfiles.parser.FlatFileParser;
import edu.nd.crc.safa.features.flatfiles.parser.TimFileParser;
import edu.nd.crc.safa.features.generation.summary.SummaryService;
import edu.nd.crc.safa.features.generation.tgen.services.TraceGenerationService;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.CommitJobUtility;
import edu.nd.crc.safa.utilities.FileUtilities;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Responsible for providing step implementations for parsing flat files
 * to use the project creation worker.
 */
public class FlatFileProjectCreationJob extends CommitJob {

    /**
     * Whether code artifacts should be summarized if no summary exists.
     */
    private final boolean shouldSummarize;
    /**
     * Whether job is updating project.
     */
    private final boolean isNewProject;
    /**
     * Path to Tim file upload.
     */
    private String pathToTIMFile;
    /**
     * The parser used to parse time file.
     */
    private FlatFileParser flatFileParser;
    /**
     * Path to uploaded files.
     */
    private String pathToFiles;

    public FlatFileProjectCreationJob(SafaUser user,
                                      JobDbEntity jobDbEntity,
                                      ServiceProvider serviceProvider,
                                      ProjectCommitDefinition commit,
                                      String uploadedFilesPath,
                                      boolean shouldSummarize,
                                      boolean isNewProject) {
        super(user, jobDbEntity, serviceProvider, commit, isNewProject);
        this.pathToFiles = uploadedFilesPath;
        this.shouldSummarize = shouldSummarize;
        this.isNewProject = isNewProject;
    }

    @IJobStep(value = "Uploading Flat Files", position = 1)
    public void initJobData(JobLogger jobLogger) throws SafaError, IOException {
        Project project = this.getProjectCommitDefinition().getCommitVersion().getProject();
        this.pathToTIMFile = ProjectPaths.Storage.uploadedProjectFilePath(project, ProjectVariables.TIM_FILENAME);
        this.pathToFiles = ProjectPaths.Storage.projectUploadsPath(project, false);
        parseTimFile(jobLogger);
    }

    private void parseTimFile(JobLogger jobLogger) throws IOException {
        if (!Files.exists(Paths.get(this.pathToTIMFile))) {
            throw new SafaError("TIM.json file was not uploaded for this project.");
        }

        JSONObject timFileJson = tryParseTim(jobLogger);
        TimFileParser timFileParser = new TimFileParser(timFileJson, this.pathToFiles);
        this.flatFileParser = new FlatFileParser(timFileParser);
    }

    private JSONObject tryParseTim(JobLogger jobLogger) throws IOException {
        try {
            return JsonFileUtilities.readJSONFile(this.pathToTIMFile);
        } catch (JSONException | IOException e) {
            jobLogger.log("Error parsing TIM file: " + e.getMessage());
            throw e;
        }
    }

    @IJobStep(value = "Parsing Files", position = 2)
    public void parsingFiles(JobLogger logger) {
        parsingArtifactFiles(logger);
        parsingTraceFiles(logger);
    }

    public void parsingArtifactFiles(JobLogger logger) throws SafaError {
        ProjectCommitDefinition projectCommitDefinition = getProjectCommitDefinition();

        EntityParsingResult<ArtifactAppEntity, String> artifactCreationResponse = flatFileParser.parseArtifacts();
        projectCommitDefinition.getArtifacts().setAdded(artifactCreationResponse.getEntities());
        logger.log("%d artifacts created.", projectCommitDefinition.getArtifacts().getSize());

        List<CommitError> artifactErrors = createErrors(artifactCreationResponse.getErrors(), ProjectEntity.ARTIFACTS);
        projectCommitDefinition.getErrors().addAll(artifactErrors);
        logger.log("%d errors found.", projectCommitDefinition.getErrors().size());
    }

    public void parsingTraceFiles(JobLogger logger) throws SafaError {
        ProjectCommitDefinition projectCommitDefinition = getProjectCommitDefinition();

        List<ArtifactAppEntity> artifactsCreated = projectCommitDefinition.getArtifacts().getAdded();
        EntityParsingResult<TraceAppEntity, String> traceCreationResponse =
            flatFileParser.parseTraces(artifactsCreated);
        projectCommitDefinition.getTraces().setAdded(traceCreationResponse.getEntities());
        logger.log("%d traces created.", projectCommitDefinition.getTraces().getSize());

        List<CommitError> traceErrors = createErrors(traceCreationResponse.getErrors(), ProjectEntity.TRACES);
        projectCommitDefinition.getErrors().addAll(traceErrors);
        logger.log("%d errors found.", projectCommitDefinition.getErrors().size());
    }

    private List<CommitError> createErrors(List<String> errorMessages,
                                           ProjectEntity projectEntity) {
        CommitErrorRepository commitErrorRepository = this.getServiceProvider().getCommitErrorRepository();
        ProjectVersion projectVersion = this.getProjectCommitDefinition().getCommitVersion();
        return
            errorMessages
                .stream()
                .map(e -> new CommitError(projectVersion, e, projectEntity))
                .map(commitErrorRepository::save)
                .collect(Collectors.toList());
    }

    @IJobStep(value = "Summarizing Code Artifacts", position = 3)
    public void summarizeCodeArtifacts() {
        if (!this.shouldSummarize) {
            return;
        }
        ProjectCommitDefinition projectCommitDefinition = this.getProjectCommitDefinition();
        List<ArtifactAppEntity> newArtifacts = projectCommitDefinition.getArtifacts().getAdded();
        SummaryService summaryService = this.getServiceProvider().getSummaryService();
        summaryService.addSummariesToCode(newArtifacts, null, this.getDbLogger());
        projectCommitDefinition.getArtifacts().setAdded(newArtifacts);
    }

    @IJobStep(value = "Generating Trace Links", position = 4)
    public void generatingTraces(JobLogger logger) {
        getServiceProvider().getPermissionService()
            .requirePermission(ProjectPermission.GENERATE, getProjectVersion().getProject(), getUser());

        ProjectCommitDefinition projectCommitDefinition = getProjectCommitDefinition();

        TraceGenerationService traceGenerationService = this.getServiceProvider().getTraceGenerationService();
        ProjectAppEntity projectAppEntity = new ProjectAppEntity(projectCommitDefinition);
        List<TraceAppEntity> generatedLinks = traceGenerationService.generateTraceLinks(
            flatFileParser.getTGenRequestAppEntity(),
            projectAppEntity);
        List<TraceAppEntity> addedTraceLinks = projectCommitDefinition.getTraces().getAdded();
        generatedLinks = traceGenerationService.removeOverlappingLinks(addedTraceLinks, generatedLinks);
        logger.log("%d traces generated.", generatedLinks.size());

        projectCommitDefinition.getTraces().getAdded().addAll(generatedLinks);
    }

    @Override
    protected void jobFailed(Exception error) throws RuntimeException, IOException {
        if (this.isNewProject) {
            CommitJobUtility.deleteCommitProject(this);
        }
    }

    @Override
    protected void afterJob(boolean success) throws Exception {
        FileUtilities.deletePath(this.pathToFiles);
    }
}
