package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.EntityParsingResult;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.errors.repositories.CommitErrorRepository;
import edu.nd.crc.safa.features.flatfiles.parser.FlatFileParser;
import edu.nd.crc.safa.features.flatfiles.parser.TimFileParser;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntity;
import edu.nd.crc.safa.features.tgen.generator.TraceGenerationService;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Responsible for providing step implementations for parsing flat files
 * to use the project creation worker.
 */
public class FlatFileProjectCreationJob extends CommitJob {

    /**
     * The initial project version
     */
    private ProjectVersion projectVersion;

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

    private String projectName;
    private String projectDescription;
    private SafaUser user;

    public FlatFileProjectCreationJob(JobDbEntity jobDbEntity,
                                      ServiceProvider serviceProvider,
                                      ProjectVersion projectVersion) {
        super(jobDbEntity, serviceProvider, new ProjectCommit(projectVersion, true));
        this.projectVersion = projectVersion;
    }

    public FlatFileProjectCreationJob(JobDbEntity jobDbEntity,
                                      ServiceProvider serviceProvider,
                                      SafaUser user,
                                      String projectName,
                                      String projectDescription,
                                      String uploadedFilesPath) {
        super(jobDbEntity, serviceProvider);
        this.projectName = projectName;
        this.projectDescription = projectDescription;
        this.pathToFiles = uploadedFilesPath;
        this.user = user;
    }

    private void createProject() throws IOException {
        this.projectVersion = createProject(user, projectName, projectDescription);
        String projectPath = ProjectPaths.Storage.projectPath(this.projectVersion.getProject(), true);
        Files.move(Path.of(this.pathToFiles), Path.of(projectPath), StandardCopyOption.REPLACE_EXISTING);
    }

    @IJobStep(value = "Uploading Flat Files", position = 1)
    public void initJobData(JobLogger jobLogger) throws SafaError, IOException {
        if (this.projectVersion == null) {
            createProject();
        }

        Project project = this.projectVersion.getProject();
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
        ProjectCommit projectCommit = getProjectCommit();

        EntityParsingResult<ArtifactAppEntity, String> artifactCreationResponse = flatFileParser.parseArtifacts();
        projectCommit.getArtifacts().setAdded(artifactCreationResponse.getEntities());
        logger.log("%d artifacts created.", projectCommit.getArtifacts().getSize());

        List<CommitError> artifactErrors = createErrors(artifactCreationResponse.getErrors(), ProjectEntity.ARTIFACTS);
        projectCommit.getErrors().addAll(artifactErrors);
        logger.log("%d errors found.", projectCommit.getErrors().size());
    }

    public void parsingTraceFiles(JobLogger logger) throws SafaError {
        ProjectCommit projectCommit = getProjectCommit();

        List<ArtifactAppEntity> artifactsCreated = projectCommit.getArtifacts().getAdded();
        EntityParsingResult<TraceAppEntity, String> traceCreationResponse =
            flatFileParser.parseTraces(artifactsCreated);
        projectCommit.getTraces().setAdded(traceCreationResponse.getEntities());
        logger.log("%d traces created.", projectCommit.getTraces().getSize());

        List<CommitError> traceErrors = createErrors(traceCreationResponse.getErrors(), ProjectEntity.TRACES);
        projectCommit.getErrors().addAll(traceErrors);
        logger.log("%d errors found.", projectCommit.getErrors().size());
    }

    private List<CommitError> createErrors(List<String> errorMessages,
                                           ProjectEntity projectEntity) {
        CommitErrorRepository commitErrorRepository = this.serviceProvider.getCommitErrorRepository();
        return
            errorMessages
                .stream()
                .map(e -> new CommitError(projectVersion, e, projectEntity))
                .map(commitErrorRepository::save)
                .collect(Collectors.toList());
    }

    @IJobStep(value = "Generating Trace Links", position = 3)
    public void generatingTraces(JobLogger logger) {
        ProjectCommit projectCommit = getProjectCommit();

        TraceGenerationService traceGenerationService = this.getServiceProvider().getTraceGenerationService();
        ProjectAppEntity projectAppEntity = new ProjectAppEntity(projectCommit);
        List<TraceAppEntity> generatedLinks = traceGenerationService.generateTraceLinks(
            flatFileParser.getTraceGenerationRequest(),
            projectAppEntity);
        generatedLinks = traceGenerationService.filterDuplicateGeneratedLinks(projectCommit.getTraces().getAdded(),
            generatedLinks);
        logger.log("%d traces generated.", generatedLinks.size());

        projectCommit.getTraces().getAdded().addAll(generatedLinks);
    }
}
