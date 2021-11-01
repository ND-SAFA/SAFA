package edu.nd.crc.safa.server.controllers;

import java.util.Optional;
import java.util.UUID;
import javax.validation.Valid;

import edu.nd.crc.safa.server.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.messages.ProjectCreationResponse;
import edu.nd.crc.safa.server.messages.ServerError;
import edu.nd.crc.safa.server.messages.ServerResponse;
import edu.nd.crc.safa.server.services.ProjectService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@CrossOrigin
@RestController
public class ProjectController extends BaseController {

    private final ProjectService projectService;

    @Autowired
    public ProjectController(ProjectRepository projectRepository,
                             ProjectVersionRepository projectVersionRepository,
                             ProjectService projectService) {
        super(projectRepository, projectVersionRepository);
        this.projectService = projectService;
    }

    @PostMapping("projects")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createOrUpdateProject(@Valid @RequestBody ProjectAppEntity payload) throws ServerError {
        Project project = Project.fromAppEntity(payload); // gets
        ProjectVersion projectVersion = payload.projectVersion;

        ProjectCreationResponse response;
        if (!project.hasDefinedId()) { // new projects expected to have no projectId or projectVersion
            response = createNewProjectWithVersion(project, projectVersion, payload);
        } else {
            response = updateProjectAtVersion(project, projectVersion, payload);
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

    private ProjectCreationResponse updateProjectAtVersion(Project project,
                                                           ProjectVersion projectVersion,
                                                           ProjectAppEntity payload) throws ServerError {
        ProjectCreationResponse response;
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
        return response;
    }

    private ProjectCreationResponse createNewProjectWithVersion(
        Project project,
        ProjectVersion projectVersion,
        ProjectAppEntity payload) throws ServerError {
        ProjectCreationResponse response;
        if (projectVersion != null
            && projectVersion.hasValidVersion()
            && projectVersion.hasValidId()) {
            throw new ServerError("Invalid ProjectVersion: cannot be defined when creating a new project.");
        }
        project = createProjectIdentifier(project.getName(), project.getDescription());
        projectVersion = createProjectVersion(project);
        response = this.projectService.saveProjectAppEntity(projectVersion, payload);
        return response;
    }


}
