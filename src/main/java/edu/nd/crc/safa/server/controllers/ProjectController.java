package edu.nd.crc.safa.server.controllers;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.db.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.repositories.ProjectRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.messages.ProjectCreationResponse;
import edu.nd.crc.safa.server.messages.ServerError;
import edu.nd.crc.safa.server.messages.ServerResponse;
import edu.nd.crc.safa.server.services.FlatFileService;
import edu.nd.crc.safa.server.services.ProjectService;

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

    @Autowired
    public ProjectController(ProjectRepository projectRepository,
                             ProjectVersionRepository projectVersionRepository,
                             ProjectService projectService,
                             FlatFileService flatFileService) {
        super(projectRepository, projectVersionRepository);
        this.projectService = projectService;
        this.flatFileService = flatFileService;
    }

    @PostMapping(value = "projects/{projectId}/{versionId}/flat-files")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse updateProjectVersionFromFlatFiles(
        @PathVariable UUID projectId,
        @PathVariable UUID versionId,
        @RequestParam MultipartFile[] files) throws ServerError {
        if (files.length == 0) {
            throw new ServerError("Could not create project because no files were received.");
        }

        Optional<Project> project = this.projectRepository.findById(projectId);
        if (!project.isPresent()) {
            String message = String.format("Could not find project with id: %s", projectId);
            throw new ServerError(message);
        }
        Optional<ProjectVersion> projectVersion = this.projectVersionRepository.findById(versionId);
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

        Project project = createProject(null, null);
        ProjectVersion projectVersion = createProjectVersion(project);

        ProjectCreationResponse response = this.flatFileService.parseAndUploadFlatFiles(project,
            projectVersion,
            files);
        return new ServerResponse(response);
    }

    @PostMapping("projects/")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createOrUpdateProject(@RequestBody ProjectAppEntity payload) throws ServerError {
        Project project = Project.fromAppEntity(payload); // gets
        ProjectVersion projectVersion = payload.projectVersion;

        ProjectCreationResponse response;
        if (!project.hasDefinedId()) { // new projects expected to have no projectId or projectVersion
            if (projectVersion != null
                && projectVersion.hasValidVersion()
                && projectVersion.hasValidId()) {
                throw new ServerError("Invalid ProjectVersion: cannot be defined when creating a new project.");
            }
            project = createProject(project.getName(), project.getDescription());
            projectVersion = createProjectVersion(project);
            response = this.projectService.createProject(projectVersion, payload);
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

    @GetMapping("projects/")
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

    private Project createProject(String name, String description) {
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
