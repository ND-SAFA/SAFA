package edu.nd.crc.safa.server.controllers;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.db.repositories.ProjectRepository;
import edu.nd.crc.safa.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.responses.ProjectAndVersion;
import edu.nd.crc.safa.server.responses.ProjectCreationResponse;
import edu.nd.crc.safa.server.responses.ServerError;
import edu.nd.crc.safa.server.responses.ServerResponse;
import edu.nd.crc.safa.server.services.FlatFileService;
import edu.nd.crc.safa.server.services.ProjectService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.CrossOrigin;
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

    @Autowired
    public ProjectController(ProjectRepository projectRepository,
                             ProjectVersionRepository projectVersionRepository,
                             ProjectService projectService,
                             FlatFileService flatFileService) {
        super(projectRepository, projectVersionRepository);
        this.projectService = projectService;
        this.flatFileService = flatFileService;
    }

    @PostMapping(value = "projects/flat-files/{projectId}/{versionId}")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse updateProjectVersionFromFlatFiles(
        @PathVariable String projectId,
        @PathVariable String versionId,
        @RequestParam MultipartFile[] files) throws ServerError {
        if (files.length == 0) {
            throw new ServerError("Could not create project because no files were received.");
        }

        Optional<Project> project = this.projectRepository.findById(UUID.fromString(projectId));
        if (!project.isPresent()) {
            String message = String.format("Could not find project with id: %s", projectId);
            throw new ServerError(message);
        }
        Optional<ProjectVersion> projectVersion = this.projectVersionRepository.findById(UUID.fromString(versionId));
        if (!projectVersion.isPresent()) {
            String message = String.format("Could not find ProjectVersion with id: %s", versionId);
            throw new ServerError(message);
        }

        ProjectCreationResponse response = this.flatFileService.parseAndUploadFlatFiles(
            project.get(),
            projectVersion.get(),
            files);
        return new ServerResponse(response);
    }

    @PostMapping(value = "projects/flat-files")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createNewProjectFromFlatFiles(@RequestParam MultipartFile[] files) throws ServerError {
        if (files.length == 0) {
            throw new ServerError("Could not create project because no files were received.");
        }

        Project project = createProject(null);
        ProjectVersion projectVersion = createProjectVersion(project);

        ProjectCreationResponse response = this.flatFileService.parseAndUploadFlatFiles(project,
            projectVersion,
            files);
        return new ServerResponse(response);
    }

    @PostMapping("projects/")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createOrUpdateProject(@RequestBody ProjectAndVersion payload) throws ServerError {
        ProjectCreationResponse response;

        Project project = Project.fromAppEntity(payload.project); // gets
        ProjectVersion projectVersion = payload.projectVersion;

        if (!project.hasDefinedId()) { // new projects expected to have no projectId or projectVersion
            if (projectVersion != null
                && projectVersion.hasValidVersion()
                && projectVersion.hasValidId()) {
                throw new ServerError("Invalid ProjectVersion: cannot be defined when creating a new project.");
            }
            project = createProject(project.getName());
            projectVersion = createProjectVersion(project);
            response = this.projectService.createProject(projectVersion, payload.project);
        } else {
            if (!projectVersion.hasValidId()) {
                throw new ServerError("Invalid Project version: must have a valid ID.");
            } else if (!projectVersion.hasValidVersion()) {
                throw new ServerError("Invalid Project version: must contain positive major, minor, and revision "
                    + "numbers.");
            }
            this.projectRepository.save(project);
            projectVersion.setProject(project);
            this.projectVersionRepository.save(projectVersion);
            response = this.projectService.updateProject(projectVersion, payload.project);
        }

        return new ServerResponse(response);
    }

    @CrossOrigin
    @GetMapping("projects/")
    public ServerResponse getProjects() {
        return new ServerResponse(this.projectRepository.findAll());
    }

    private Project createProject(String name) {
        Project project = new Project(name); // TODO: extract name from TIM file
        this.projectRepository.save(project);
        return project;
    }

    private ProjectVersion createProjectVersion(Project project) {
        ProjectVersion projectVersion = new ProjectVersion(project, 1, 1, 1);
        this.projectVersionRepository.save(projectVersion);
        return projectVersion;
    }
}
