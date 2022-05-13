package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.UUID;
import javax.validation.Valid;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.api.ProjectIdentifier;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.projects.ProjectRepository;
import edu.nd.crc.safa.server.services.ProjectService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for creating and updating project entities via JSON.
 */
@RestController
public class ProjectController extends BaseController {

    private final ProjectRepository projectRepository;
    private final ProjectService projectService;

    @Autowired
    public ProjectController(ResourceBuilder resourceBuilder,
                             ProjectRepository projectRepository,
                             ProjectService projectService) {
        super(resourceBuilder);
        this.projectRepository = projectRepository;
        this.projectService = projectService;
    }

    /**
     * Creates or updates project given creating or updating defined entities (e.g. artifacts, traces). Note, artifacts
     * not specified are assumed to be removed if version is specified.
     *
     * @param project The project entity containing artifacts, traces, name, and descriptions.
     * @return The project and associated entities created.
     * @throws SafaError Throws error if a database violation occurred while creating or updating any entities in
     *                   payload.
     */
    @PostMapping(AppRoutes.Projects.createOrUpdateProjects)
    @ResponseStatus(HttpStatus.CREATED)
    public ProjectEntities createOrUpdateProject(@RequestBody @Valid ProjectAppEntity project) throws SafaError {
        Project payloadProject = Project.fromAppEntity(project);
        ProjectVersion payloadProjectVersion = project.projectVersion;

        ProjectEntities projectEntities;
        if (!payloadProject.hasDefinedId()) { // new projects expected to have no projectId or projectVersion
            if (payloadProjectVersion != null
                && payloadProjectVersion.hasValidVersion()
                && payloadProjectVersion.hasValidId()) {
                throw new SafaError("Invalid ProjectVersion: cannot be defined when creating a new project.");
            }
            projectEntities = this.projectService.createNewProjectWithVersion(payloadProject, project);
        } else {
            this.resourceBuilder.fetchProject(payloadProject.getProjectId()).withEditProject();
            projectEntities = this.projectService.updateProjectAtVersion(
                payloadProject, payloadProjectVersion, project);
        }

        return projectEntities;
    }

    /**
     * Returns list of all project identifiers present in the database.
     *
     * @return List of project identifiers.
     */
    @GetMapping(AppRoutes.Projects.Membership.getUserProjects)
    public List<ProjectIdentifier> getUserProjects() {
        return projectService.getCurrentUserProjects();
    }

    /**
     * Deletes project with associated projectId.
     *
     * @param projectId UUID of project to delete.
     * @throws SafaError Throws error if project with associated id is not found.
     */
    @DeleteMapping(AppRoutes.Projects.deleteProjectById)
    @ResponseStatus(HttpStatus.OK)
    public void deleteProject(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withOwnProject();
        this.projectRepository.delete(project);
    }
}
