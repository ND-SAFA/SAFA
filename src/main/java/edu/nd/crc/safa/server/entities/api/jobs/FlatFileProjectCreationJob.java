package edu.nd.crc.safa.server.entities.api.jobs;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.common.EntityCreation;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.flatfiles.entities.TimParser;
import edu.nd.crc.safa.flatfiles.services.FileService;
import edu.nd.crc.safa.flatfiles.services.FlatFileService;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.ServiceProvider;

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
    TimParser timParser;
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
        FileService fileService = this.serviceProvider.getFileService();
        fileService.uploadFilesToServer(project, Arrays.asList(files));
        this.pathToTIMFile = ProjectPaths.getPathToFlatFile(project, ProjectVariables.TIM_FILENAME);
    }

    private void parseTimFile() {
        if (!Files.exists(Paths.get(this.pathToTIMFile))) {
            throw new SafaError("TIM.json file was not uploaded for this project");
        }

        try {
            String timFileContent = new String(Files.readAllBytes(Paths.get(this.pathToTIMFile)));
            JSONObject timFileJson = new JSONObject(timFileContent);
            this.timParser = new TimParser(timFileJson, this.pathToFiles);
        } catch (Exception e) {
            throw new SafaError("Could not parse");
        }
    }

    public void parsingArtifactFiles() throws SafaError {
        EntityCreation<ArtifactAppEntity, String> artifactCreationResponse = timParser.parseArtifacts();
        projectCommit.getArtifacts().setAdded(artifactCreationResponse.getEntities());
        List<CommitError> errors = createErrors(artifactCreationResponse.getErrors(), ProjectEntity.ARTIFACTS);
        projectCommit.getErrors().addAll(errors);
    }

    public void parsingTraceFiles() throws SafaError {
        ProjectAppEntity projectAppEntity = new ProjectAppEntity();
        projectAppEntity.getArtifacts().addAll(projectCommit.getArtifacts().getAdded());
        EntityCreation<TraceAppEntity, String> traceCreationResponse = timParser.parseTraces(projectAppEntity);
        projectCommit.getTraces().setAdded(traceCreationResponse.getEntities());
        List<CommitError> errors = createErrors(traceCreationResponse.getErrors(), ProjectEntity.TRACES);
        projectCommit.getErrors().addAll(errors);
    }

    private List<CommitError> createErrors(List<String> errorMessages,
                                           ProjectEntity projectEntity) {
        return
            errorMessages
                .stream()
                .map(e -> new CommitError(projectVersion, e, projectEntity))
                .collect(Collectors.toList());
    }

    public void generatingTraces() {
        FlatFileService flatFileService = this.getServiceProvider().getFlatFileService();
        List<TraceAppEntity> generatedLinks = flatFileService.generateTraceLinks(
            projectCommit.getArtifacts().getAdded(),
            timParser.getTraceGenerationRequests());
        generatedLinks = flatFileService.filterDuplicateGeneratedLinks(projectCommit.getTraces().getAdded(),
            generatedLinks);
        projectCommit.getTraces().getAdded().addAll(generatedLinks);
    }
}
