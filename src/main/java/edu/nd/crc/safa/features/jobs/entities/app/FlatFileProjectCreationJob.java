package edu.nd.crc.safa.features.jobs.entities.app;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.common.EntityParsingResult;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.errors.repositories.CommitErrorRepository;
import edu.nd.crc.safa.features.flatfiles.parser.FlatFileParser;
import edu.nd.crc.safa.features.flatfiles.parser.TimFileParser;
import edu.nd.crc.safa.features.flatfiles.services.FlatFileService;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.FileUtilities;

import org.json.JSONObject;
import org.springframework.web.multipart.MultipartFile;

/**
 * Responsible for providing step implementations for parsing flat files
 * to use the project creation worker.
 */
public class FlatFileProjectCreationJob extends CommitJob {

    /**
     * The initial project version
     */
    ProjectVersion projectVersion;
    /**
     * The files being parsed into a project.
     */
    MultipartFile[] files;
    /**
     * Path to Tim file upload.
     */
    String pathToTIMFile;
    /**
     * The parser used to parse time file.
     */
    FlatFileParser flatFileParser;
    /**
     * Path to uploaded files.
     */
    String pathToFiles;

    public FlatFileProjectCreationJob(JobDbEntity jobDbEntity,
                                      ServiceProvider serviceProvider,
                                      ProjectVersion projectVersion,
                                      MultipartFile[] files) {
        super(jobDbEntity, serviceProvider, new ProjectCommit(projectVersion, true));
        this.projectVersion = projectVersion;
        this.files = files;
    }

    @Override
    @IJobStep(name = "Uploading Flat Files", position = 1)
    public void initJobData() throws SafaError, IOException {
        super.initJobData();
        Project project = this.projectVersion.getProject();
        this.pathToTIMFile = ProjectPaths.Storage.uploadedProjectFilePath(project, ProjectVariables.TIM_FILENAME);
        this.pathToFiles = ProjectPaths.Storage.projectUploadsPath(project, false);
        parseTimFile();
    }

    private void parseTimFile() throws IOException {
        if (!Files.exists(Paths.get(this.pathToTIMFile))) {
            throw new SafaError("TIM.json file was not uploaded for this project");
        }

        JSONObject timFileJson = FileUtilities.readJSONFile(this.pathToTIMFile);
        TimFileParser timFileParser = new TimFileParser(timFileJson, this.pathToFiles);
        this.flatFileParser = new FlatFileParser(timFileParser);
    }

    @IJobStep(name = "Parsing Files", position = 2)
    public void parsingFiles() {
        parsingArtifactFiles();
        parsingTraceFiles();
    }

    public void parsingArtifactFiles() throws SafaError {
        EntityParsingResult<ArtifactAppEntity, String> artifactCreationResponse = flatFileParser.parseArtifacts();
        projectCommit.getArtifacts().setAdded(artifactCreationResponse.getEntities());
        List<CommitError> artifactErrors = createErrors(artifactCreationResponse.getErrors(), ProjectEntity.ARTIFACTS);
        projectCommit.getErrors().addAll(artifactErrors);
    }

    public void parsingTraceFiles() throws SafaError {
        List<ArtifactAppEntity> artifactsCreated = projectCommit.getArtifacts().getAdded();
        EntityParsingResult<TraceAppEntity, String> traceCreationResponse =
            flatFileParser.parseTraces(artifactsCreated);
        projectCommit.getTraces().setAdded(traceCreationResponse.getEntities());
        List<CommitError> traceErrors = createErrors(traceCreationResponse.getErrors(), ProjectEntity.TRACES);
        projectCommit.getErrors().addAll(traceErrors);
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

    @IJobStep(name = "Generating Trace Links", position = 3)
    public void generatingTraces() {
        FlatFileService flatFileService = this.getServiceProvider().getFlatFileService();
        List<TraceAppEntity> generatedLinks = flatFileService.generateTraceLinks(
            projectCommit.getArtifacts().getAdded(),
            flatFileParser.getTraceGenerationRequests());
        generatedLinks = flatFileService.filterDuplicateGeneratedLinks(projectCommit.getTraces().getAdded(),
            generatedLinks);
        projectCommit.getTraces().getAdded().addAll(generatedLinks);
    }
}
