package edu.nd.crc.safa.features.projects.controllers;

import static edu.nd.crc.safa.utilities.AssertUtils.assertNotNull;
import static edu.nd.crc.safa.utilities.AssertUtils.assertNull;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.memberships.services.ProjectMembershipService;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;
import edu.nd.crc.safa.features.organizations.services.TeamService;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectIdAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for creating and updating project entities via JSON.
 */
@RestController
public class ProjectController extends BaseController {

    private final ProjectMembershipService projectMembershipService;
    private final OrganizationService organizationService;
    private final TeamService teamService;

    @Autowired
    public ProjectController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                             ProjectMembershipService projectMembershipService, OrganizationService organizationService,
                             TeamService teamService) {
        super(resourceBuilder, serviceProvider);
        this.projectMembershipService = projectMembershipService;
        this.organizationService = organizationService;
        this.teamService = teamService;
    }

    /**
     * Creates or updates project identifier information via JSON.
     * Project is created if no project ID is given. Otherwise, update is assumed.
     *
     * @param projectAppEntity The project entity containing artifacts, traces, name, and descriptions.
     * @return The project and associated entities created.
     * @throws SafaError Throws error if a database violation occurred while creating or updating any entities in
     *                   payload.
     */
    @PostMapping(AppRoutes.Projects.CREATE_OR_UPDATE_PROJECT_META)
    @ResponseStatus(HttpStatus.CREATED)
    public ProjectAppEntity createProject(@RequestBody @Valid ProjectAppEntity projectAppEntity) throws SafaError {
        assertNull(projectAppEntity.getProjectId(), "Cannot specify project ID during project creation.");
        assertNull(projectAppEntity.getProjectVersion(), "Cannot specify project version during project creation");

        // Step - Create project identifier
        Project projectEntity = createProjectFromAppEntity(projectAppEntity);
        projectAppEntity.setProjectId(projectEntity.getProjectId());

        // Step - Create version
        ProjectVersion projectVersion = getServiceProvider()
            .getVersionService()
            .createInitialProjectVersion(projectEntity);
        projectAppEntity.setProjectVersion(projectVersion);

        return projectAppEntity;
    }

    /**
     * Creates or updates project identifier information via JSON.
     * Project is created if no project ID is given. Otherwise, update is assumed.
     *
     * @param projectAppEntity The project entity containing artifacts, traces, name, and descriptions.
     * @return The project and associated entities created.
     * @throws SafaError Throws error if a database violation occurred while creating or updating any entities in
     *                   payload.
     */
    @PutMapping(AppRoutes.Projects.CREATE_OR_UPDATE_PROJECT_META)
    public ProjectAppEntity updateProject(@RequestBody @Valid ProjectAppEntity projectAppEntity) throws SafaError {
        assertNotNull(projectAppEntity.getProjectId(), "Missing project ID");

        // Step - Finding project identifier
        UUID projectId = projectAppEntity.getProjectId();
        Project project = getServiceProvider().getProjectRepository().findByProjectId(projectId);

        // Step - Update meta information
        project.updateFromAppEntity(projectAppEntity);
        getServiceProvider().getProjectRepository().save(project);

        return projectAppEntity;
    }

    /**
     * Create a project based on the values sent from the front end. If a team ID is specified,
     * create a project within the team with that ID. Otherwise, if an organization ID is specified,
     * create a project within the organization with that ID (under the full-org team). Otherwise,
     * create a project owned by the current user (within their personal org/team).
     *
     * @param projectAppEntity The project definition from the front end
     * @return A newly created project object
     */
    private Project createProjectFromAppEntity(ProjectAppEntity projectAppEntity) {
        ProjectService projectService = getServiceProvider().getProjectService();

        if (projectAppEntity.getTeamId() != null) {
            Team team = teamService.getTeamById(projectAppEntity.getTeamId());
            return projectService.createProject(projectAppEntity, team);
        } else if (projectAppEntity.getOrgId() != null) {
            Organization organization = organizationService.getOrganizationById(projectAppEntity.getOrgId());
            return projectService.createProject(projectAppEntity, organization);
        } else {
            SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
            return projectService.createProject(projectAppEntity, user);
        }
    }

    /**
     * Returns list of all project identifiers present in the database.
     *
     * @return List of project identifiers.
     */
    @GetMapping(AppRoutes.Projects.Membership.GET_USER_PROJECTS)
    public List<ProjectIdAppEntity> getUserProjects() {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        return projectMembershipService.getProjectIdAppEntitiesForUser(user);
    }

    /**
     * Deletes project with associated projectId.
     *
     * @param projectId UUID of project to delete.
     * @throws SafaError Throws error if project with associated id is not found.
     */
    @DeleteMapping(AppRoutes.Projects.DELETE_PROJECT_BY_ID)
    @ResponseStatus(HttpStatus.OK)
    public void deleteProject(@PathVariable UUID projectId) throws SafaError {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        Project project = getResourceBuilder().fetchProject(projectId)
            .withPermission(ProjectPermission.DELETE, user).get();
        getServiceProvider().getProjectRepository().delete(project);
    }
}
