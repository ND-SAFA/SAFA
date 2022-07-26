package edu.nd.crc.safa.server.entities.api.jobs;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.common.EntityParsingResult;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.flatfiles.entities.FlatFileParser;
import edu.nd.crc.safa.flatfiles.services.FileUploadService;
import edu.nd.crc.safa.flatfiles.services.FlatFileService;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.CommitErrorRepository;
import edu.nd.crc.safa.server.services.ServiceProvider;
import edu.nd.crc.safa.utilities.FileUtilities;

import org.json.JSONObject;
import org.springframework.web.multipart.MultipartFile;

/**
 * Responsible for providing step implementations for parsing flat files
 * to use the project creation worker.
 * TODO: Implement default spring steps.
 */
public class FlatFileProjectCreationJob extends ProjectCreationJob {

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
    public void initJobData() throws SafaError {
        super.initJobData();
        Project project = this.projectVersion.getProject();
        uploadFlatFiles(project);
        this.pathToFiles = ProjectPaths.getPathToUploadedFiles(project, false);
        parseTimFile();
    }

    private void uploadFlatFiles(Project project) {
        FileUploadService fileUploadService = this.serviceProvider.getFileUploadService();
        fileUploadService.uploadFilesToServer(project, Arrays.asList(files));
        this.pathToTIMFile = ProjectPaths.getPathToFlatFile(project, ProjectVariables.TIM_FILENAME);
    }

    private void parseTimFile() {
        if (!Files.exists(Paths.get(this.pathToTIMFile))) {
            throw new SafaError("TIM.json file was not uploaded for this project");
        }

        try {
            JSONObject timFileJson = FileUtilities.readJSONFile(this.pathToTIMFile);
            this.flatFileParser = new FlatFileParser(timFileJson, this.pathToFiles);
        } catch (Exception e) {
            throw new SafaError("Could not parse");
        }
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
