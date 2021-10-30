package edu.nd.crc.safa.server.controllers;

import java.io.IOException;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;
import javax.validation.Valid;

import edu.nd.crc.safa.importer.flatfiles.ArtifactFileParser;
import edu.nd.crc.safa.importer.flatfiles.TraceFileParser;
import edu.nd.crc.safa.server.db.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.db.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.db.entities.app.TraceApplicationEntity;
import edu.nd.crc.safa.server.db.entities.sql.Artifact;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.repositories.ProjectRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.messages.ParseArtifactFileResponse;
import edu.nd.crc.safa.server.messages.ParseTraceFileResponse;
import edu.nd.crc.safa.server.messages.ProjectCreationResponse;
import edu.nd.crc.safa.server.messages.ServerError;
import edu.nd.crc.safa.server.messages.ServerResponse;
import edu.nd.crc.safa.server.services.FlatFileService;
import edu.nd.crc.safa.server.services.ProjectService;
import edu.nd.crc.safa.server.services.RevisionNotificationService;
import edu.nd.crc.safa.utilities.FileUtilities;

import org.apache.commons.csv.CSVParser;
import org.javatuples.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@CrossOrigin
@RestController
public class ProjectController extends BaseController {

    private final ProjectService projectService;
    private final FlatFileService flatFileService;
    private final RevisionNotificationService revisionNotificationService;
    private final ArtifactFileParser artifactFileParser;
    private final TraceFileParser traceFileParser;

    @Autowired
    public ProjectController(ProjectRepository projectRepository,
                             ProjectVersionRepository projectVersionRepository,
                             ProjectService projectService,
                             FlatFileService flatFileService,
                             RevisionNotificationService revisionNotificationService,
                             ArtifactFileParser artifactFileParser,
                             TraceFileParser traceFileParser) {
        super(projectRepository, projectVersionRepository);
        this.projectService = projectService;
        this.flatFileService = flatFileService;
        this.revisionNotificationService = revisionNotificationService;
        this.artifactFileParser = artifactFileParser;
        this.traceFileParser = traceFileParser;
    }

    /**
     * Uploads and parses given flat files to the specified version.
     *
     * @param versionId - The id of the version that will be modified by given files.
     * @param files     - The flat files containing tim.json, artifact files, and trace link files.
     * @return ServerResponse whose body contains all entities in project created.
     * @throws ServerError - If no files are given.
     */
    @PostMapping(value = "projects/versions/{versionId}/flat-files")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse updateProjectVersionFromFlatFiles(
        @PathVariable UUID versionId,
        @RequestParam MultipartFile[] files) throws ServerError {
        if (files.length == 0) {
            throw new ServerError("Could not create project because no files were received.");
        }
        ProjectVersion projectVersion = this.projectVersionRepository.findByVersionId(versionId);
        Project project = projectVersion.getProject();
        ProjectCreationResponse response = this.flatFileService.parseAndUploadFlatFiles(
            project,
            projectVersion,
            files);
        this.revisionNotificationService.broadcastUpdateProject(projectVersion);
        return new ServerResponse(response);
    }

    @PostMapping(value = "projects/parse/artifacts/{artifactType}")
    @ResponseStatus(HttpStatus.OK)
    public ServerResponse parseArtifactFile(@PathVariable String artifactType,
                                            @RequestParam MultipartFile file) throws ServerError, IOException {
        CSVParser fileCSV = FileUtilities.readMultiPartFile(file);
        ParseArtifactFileResponse response = new ParseArtifactFileResponse();
        Pair<List<ArtifactAppEntity>, List<String>> parseResponse =
            artifactFileParser.parseArtifactFileIntoApplicationEntities(
                file.getOriginalFilename(),
                artifactType,
                fileCSV);
        response.setArtifacts(parseResponse.getValue0());
        response.setErrors(parseResponse.getValue1());
        return new ServerResponse(response);
    }

    @PostMapping(value = "projects/parse/traces")
    @ResponseStatus(HttpStatus.OK)
    public ServerResponse parseTraceFile(@RequestParam MultipartFile file) throws ServerError, IOException {
        CSVParser fileCSV = FileUtilities.readMultiPartFile(file);
        ParseTraceFileResponse response = new ParseTraceFileResponse();
        Pair<List<TraceApplicationEntity>, List<Pair<String, Long>>> parseResponse =
            traceFileParser.readTraceFile(
                (a) -> Optional.of(new Artifact()), //TODO: Replace with artifacts from json
                (s, t) -> Optional.empty(), // TODO: Replace with traces from json
                fileCSV);
        List<String> errors = parseResponse.getValue1().stream().map(Pair::getValue0).collect(Collectors.toList());

        response.setTraces(parseResponse.getValue0());
        response.setErrors(errors);
        return new ServerResponse(response);
    }

    @PostMapping(value = "projects/flat-files")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createNewProjectFromFlatFiles(@RequestParam MultipartFile[] files) throws ServerError {
        if (files.length == 0) {
            throw new ServerError("Could not create project because no files were received.");
        }

        Project project = createProjectIdentifier(null, null);
        ProjectVersion projectVersion = createProjectVersion(project);

        ProjectCreationResponse response = this.flatFileService.parseAndUploadFlatFiles(project,
            projectVersion,
            files);
        this.revisionNotificationService.broadcastUpdateProject(projectVersion);
        return new ServerResponse(response);
    }

    @PostMapping("projects")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createOrUpdateProject(@Valid @RequestBody ProjectAppEntity payload) throws ServerError {
        Project project = Project.fromAppEntity(payload); // gets
        ProjectVersion projectVersion = payload.projectVersion;

        ProjectCreationResponse response;
        if (!project.hasDefinedId()) { // new projects expected to have no projectId or projectVersion
            if (projectVersion != null
                && projectVersion.hasValidVersion()
                && projectVersion.hasValidId()) {
                throw new ServerError("Invalid ProjectVersion: cannot be defined when creating a new project.");
            }
            project = createProjectIdentifier(project.getName(), project.getDescription());
            projectVersion = createProjectVersion(project);
            response = this.projectService.saveProjectAppEntity(projectVersion, payload);
        } else {
            this.projectRepository.save(project);
            //TODO: Update traces
            if (projectVersion == null) {
                if ((payload.artifacts != null
                    && payload.artifacts.size() > 0)) {
                    throw new ServerError("Cannot update artifacts because project version not defined");
                }
                response = new ProjectCreationResponse(payload, null, null, null);
            } else if (!projectVersion.hasValidId()) {
                throw new ServerError("Invalid Project version: must have a valid ID.");
            } else if (!projectVersion.hasValidVersion()) {
                throw new ServerError("Invalid Project version: must contain positive major, minor, and revision "
                    + "numbers.");
            } else {
                projectVersion.setProject(project);
                this.projectVersionRepository.save(projectVersion);
                response = this.projectService.updateProject(projectVersion, payload);
            }
        }

        return new ServerResponse(response);
    }

    @GetMapping("projects")
    public ServerResponse getProjects() {
        return new ServerResponse(this.projectRepository.findAll());
    }

    @DeleteMapping("projects/{projectId}")
    @ResponseStatus(HttpStatus.OK)
    public ServerResponse deleteProject(@PathVariable String projectId) throws ServerError {
        Optional<Project> projectQuery = this.projectRepository.findById(UUID.fromString(projectId));
        if (projectQuery.isPresent()) {
            this.projectRepository.delete(projectQuery.get());
            return new ServerResponse("Project deleted successfully");
        } else {
            throw new ServerError("Could not find project with id" + projectId);
        }
    }

    private Project createProjectIdentifier(String name, String description) {
        Project project = new Project(name, description); // TODO: extract name from TIM file
        this.projectRepository.save(project);
        return project;
    }

    private ProjectVersion createProjectVersion(Project project) {
        ProjectVersion projectVersion = new ProjectVersion(project, 1, 1, 1);
        this.projectVersionRepository.save(projectVersion);
        return projectVersion;
    }
}
