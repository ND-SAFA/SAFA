package edu.nd.crc.safa.server.entities.api.jobs;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.common.EntityCreation;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.importer.flatfiles.ArtifactFileParser;
import edu.nd.crc.safa.importer.flatfiles.FlatFileService;
import edu.nd.crc.safa.importer.flatfiles.TIMParser;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.TraceGenerationRequest;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.Job;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.FileUploadService;
import edu.nd.crc.safa.server.services.ProjectService;

import org.javatuples.Pair;
import org.json.JSONObject;
import org.springframework.web.multipart.MultipartFile;

public class FlatFileProjectCreationWorker extends ProjectCreationWorker {

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
     * The service used to create project.
     */
    ProjectService projectService;

    /**
     * The service used to store flat files while parsing.
     */
    FileUploadService fileUploadService;

    /**
     * The service used to parse flat files into entities.
     */
    FlatFileService flatFileService;

    /**
     * The parser used to parse time file.
     */
    TIMParser timParser;
    /**
     * List of trace generation requests parsed from flat files.
     */
    List<TraceGenerationRequest> traceGenerationRequests;

    public FlatFileProjectCreationWorker(Job job, ProjectVersion projectVersion, MultipartFile[] files) {
        super(job, new ProjectCommit(projectVersion, true));
        this.projectVersion = projectVersion;
        this.files = files;
        this.projectService = ProjectService.getInstance();
        this.fileUploadService = FileUploadService.getInstance();
        this.flatFileService = FlatFileService.getInstance();
    }

    @Override
    public void init() throws SafaError, IOException {
        super.init();
        Project project = this.projectVersion.getProject();
        this.fileUploadService.uploadFilesToServer(project, Arrays.asList(files));
        this.pathToTIMFile = ProjectPaths.getPathToFlatFile(project, ProjectVariables.TIM_FILENAME);
        if (!Files.exists(Paths.get(this.pathToTIMFile))) {
            throw new SafaError("TIM.json file was not uploaded for this project");
        }
        // Step - Create project parser
        String timFileContent = new String(Files.readAllBytes(Paths.get(pathToTIMFile)));
        JSONObject timFileJson = new JSONObject(timFileContent);
        this.timParser = new TIMParser(timFileJson);
        this.timParser.parse();
    }

    public void parsingArtifactFiles() throws SafaError {
        EntityCreation<ArtifactAppEntity, String> artifactCreationResponse =
            ArtifactFileParser.getInstance().parseArtifactFiles(projectVersion, this.timParser);
        projectCommit.getArtifacts().setAdded(artifactCreationResponse.getEntities());
        List<CommitError> commitErrors =
            artifactCreationResponse
                .getErrors()
                .stream()
                .map(e -> new CommitError(projectVersion, e, ProjectEntity.ARTIFACTS))
                .collect(Collectors.toList());
        projectCommit.getErrors().addAll(commitErrors);
    }

    public void parsingTraceFiles() throws SafaError {
        Pair<List<TraceAppEntity>, List<TraceGenerationRequest>> traceResponse = timParser.parseTraces(projectVersion);
        List<TraceAppEntity> traces = traceResponse.getValue0();
        projectCommit.getTraces().setAdded(traces);
        this.traceGenerationRequests = traceResponse.getValue1();
    }

    public void generatingTraces() {
        List<TraceAppEntity> generatedLinks = flatFileService.generateTraceLinks(
            projectCommit.getArtifacts().getAdded(),
            traceGenerationRequests);
        generatedLinks = flatFileService.filterDuplicateGeneratedLinks(projectCommit.getTraces().getAdded(),
            generatedLinks);
        projectCommit.getTraces().getAdded().addAll(generatedLinks);
    }
}
