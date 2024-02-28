package edu.nd.crc.safa.features.projects.services;

import java.io.IOException;
import java.util.Collection;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Stream;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.memberships.entities.db.IEntityMembership;
import edu.nd.crc.safa.features.memberships.services.ProjectMembershipService;
import edu.nd.crc.safa.features.memberships.services.TeamMembershipService;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.onboarding.services.OnboardingService;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.services.TeamService;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.permissions.entities.TeamPermission;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectIdAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.FileUtilities;

import lombok.Setter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Service;

/**
 * Responsible for updating, deleting, and retrieving project identifiers.
 */
@Service
@Scope("singleton")
public class ProjectService {

    @Setter(onMethod = @__({@Autowired}))
    private ProjectRepository projectRepository;

    @Setter(onMethod = @__({@Autowired}))
    private TeamService teamService;

    @Setter(onMethod = @__({@Autowired, @Lazy}))
    private ProjectMembershipService projectMembershipService;

    @Setter(onMethod = @__({@Autowired, @Lazy}))
    private TeamMembershipService teamMembershipService;

    @Setter(onMethod = @__({@Autowired}))
    private JobService jobService;

    @Setter(onMethod = @__({@Autowired, @Lazy}))
    private PermissionService permissionService;

    @Setter(onMethod = @__({@Autowired}))
    private NotificationService notificationService;

    @Setter(onMethod = @__({@Autowired}))
    private OnboardingService onboardingService;

    /**
     * Deletes given project and all related entities through cascade property.
     *
     * @param user    The user initiating the deletion of the project.
     * @param project The project to delete.
     * @throws SafaError Throws error if error occurs while deleting flat files.
     */
    public void deleteProject(SafaUser user, Project project) throws SafaError, IOException {
        permissionService.requireAnyPermission(
            Set.of(ProjectPermission.DELETE, TeamPermission.DELETE_PROJECTS), project, user
        );
        this.jobService.removeProjectFromJobs(project);
        this.projectRepository.delete(project);
        FileUtilities.deletePath(ProjectPaths.Storage.projectPath(project, false));
        if (user != null) { // null in testing scenarios.
            notificationService.broadcastChange(EntityChangeBuilder
                .create(user, project)
                .withProjectDelete());
        }
    }

    /**
     * Creates a new project
     *
     * @param name        The name of the project
     * @param description The description of the project
     * @param owner       The team that owns the project
     * @return The new project
     */
    public Project createProject(String name, String description, Team owner) {
        Project project = new Project(name, description, owner);
        project = this.projectRepository.save(project);
        onboardingService.updateStateProject(owner.getOrganization().getOwner(), project);
        return project;
    }

    /**
     * Creates a new project
     *
     * @param name        The name of the project
     * @param description The description of the project
     * @param owner       The user that owns the project
     * @return The new project
     */
    public Project createProject(String name, String description, SafaUser owner) {
        Team personalTeam = teamService.getPersonalTeam(owner);
        return createProject(name, description, personalTeam);
    }

    /**
     * Creates a new project
     *
     * @param name        The name of the project
     * @param description The description of the project
     * @param owner       The organization that owns the project
     * @return The new project
     */
    public Project createProject(String name, String description, Organization owner) {
        Team orgTeam = teamService.getFullOrganizationTeam(owner);
        return createProject(name, description, orgTeam);
    }

    /**
     * Creates a new project
     *
     * @param projectDefinition The definition of the project from the front end
     * @param owner             The user who will own the project
     * @return The new project
     */
    public Project createProject(ProjectAppEntity projectDefinition, SafaUser owner) {
        return createProject(projectDefinition.getName(), projectDefinition.getDescription(), owner);
    }

    /**
     * Creates a new project
     *
     * @param projectDefinition The definition of the project from the front end
     * @param owner             The organization who will own the project
     * @return The new project
     */
    public Project createProject(ProjectAppEntity projectDefinition, Organization owner) {
        return createProject(projectDefinition.getName(), projectDefinition.getDescription(), owner);
    }

    /**
     * Creates a new project
     *
     * @param projectDefinition The definition of the project from the front end
     * @param owner             The team who will own the project
     * @return The new project
     */
    public Project createProject(ProjectAppEntity projectDefinition, Team owner) {
        return createProject(projectDefinition.getName(), projectDefinition.getDescription(), owner);
    }

    /**
     * Creates a new project
     *
     * @param name The name of the project
     * @param description The description of the project
     * @param owner The team that owns the project
     * @param user The user who is creating the project (for permissions checks)
     * @return The new project
     */
    public Project createProjectAsUser(String name, String description, Team owner, SafaUser user) {
        permissionService.requirePermission(TeamPermission.CREATE_PROJECTS, owner, user);
        return createProject(name, description, owner);
    }

    /**
     * Creates a new project
     *
     * @param name The name of the project
     * @param description The description of the project
     * @param owner The user that owns the project
     * @param user The user who is creating the project (for permissions checks)
     * @return The new project
     */
    public Project createProjectAsUser(String name, String description, SafaUser owner, SafaUser user) {
        Team personalTeam = teamService.getPersonalTeam(owner);
        return createProjectAsUser(name, description, personalTeam, user);
    }

    /**
     * Creates a new project
     *
     * @param name The name of the project
     * @param description The description of the project
     * @param owner The organization that owns the project
     * @param user The user who is creating the project (for permissions checks)
     * @return The new project
     */
    public Project createProjectAsUser(String name, String description, Organization owner, SafaUser user) {
        Team orgTeam = teamService.getFullOrganizationTeam(owner);
        return createProjectAsUser(name, description, orgTeam, user);
    }

    /**
     * Creates a new project
     *
     * @param projectDefinition The definition of the project from the front end
     * @param owner The user who will own the project
     * @param user The user who is creating the project (for permissions checks)
     * @return The new project
     */
    public Project createProjectAsUser(ProjectAppEntity projectDefinition, SafaUser owner, SafaUser user) {
        return createProjectAsUser(projectDefinition.getName(), projectDefinition.getDescription(), owner, user);
    }

    /**
     * Creates a new project
     *
     * @param projectDefinition The definition of the project from the front end
     * @param owner The organization who will own the project
     * @param user The user who is creating the project (for permissions checks)
     * @return The new project
     */
    public Project createProjectAsUser(ProjectAppEntity projectDefinition, Organization owner, SafaUser user) {
        return createProjectAsUser(projectDefinition.getName(), projectDefinition.getDescription(), owner, user);
    }

    /**
     * Creates a new project
     *
     * @param projectDefinition The definition of the project from the front end
     * @param owner The team who will own the project
     * @param user The user who is creating the project (for permissions checks)
     * @return The new project
     */
    public Project createProjectAsUser(ProjectAppEntity projectDefinition, Team owner, SafaUser user) {
        return createProjectAsUser(projectDefinition.getName(), projectDefinition.getDescription(), owner, user);
    }

    /**
     * Return the list of projects that are owned by the specified team. This does not include
     * projects that are shared with the team.
     *
     * @param team The team
     * @return The projects the team owns
     */
    public List<Project> getProjectsOwnedByTeam(Team team) {
        return projectRepository.findByOwningTeam(team);
    }

    /**
     * Converts a project to a project identifier front-end object
     *
     * @param project     The project
     * @param currentUser The user making the request (so that we can properly show permissions)
     * @return The project identifier
     */
    public ProjectIdAppEntity getIdAppEntity(Project project, SafaUser currentUser) {
        List<IEntityMembership> projectMemberships =
            projectMembershipService.getMembershipsForEntity(project);

        List<IEntityMembership> teamMemberships =
            teamMembershipService.getMembershipsForEntity(project.getOwningTeam());

        Stream<MembershipAppEntity> projectMembershipAppEntities =
            projectMemberships.stream()
                .map(MembershipAppEntity::new);

        Stream<MembershipAppEntity> teamMembershipAppEntities =
            teamMemberships.stream()
                .map(MembershipAppEntity::new);

        List<MembershipAppEntity> membershipAppEntities =
            Stream.concat(projectMembershipAppEntities, teamMembershipAppEntities)
                .toList();

        List<String> permissions = getUserPermissions(project, currentUser)
            .stream()
            .filter(permission -> permission instanceof ProjectPermission)
            .map(Permission::getName)
            .toList();

        return new ProjectIdAppEntity(project, membershipAppEntities, permissions);
    }

    /**
     * Converts a collection of projects to project identifiers
     *
     * @param projects    The projects
     * @param currentUser The user making the request (so that we can properly show permissions)
     * @return A list of project identifier objects
     */
    public List<ProjectIdAppEntity> getIdAppEntities(Collection<Project> projects, SafaUser currentUser) {
        return projects.stream()
            .filter(project -> permissionService.hasAnyPermission(
                Set.of(TeamPermission.VIEW_PROJECTS, ProjectPermission.VIEW), project, currentUser
            )).map(project -> getIdAppEntity(project, currentUser))
            .toList();
    }

    /**
     * Get all permissions granted to the user via their membership(s) within the given team.
     *
     * @param project     The project the user is a part of. Note that the user can have permissions on a project even
     *                    if they do not have a direct project membership, as they could be a member of a team or an
     *                    organization that grants them project permissions.
     * @param currentUser The user in question
     * @return A list of permissions the user has for the project
     */
    public List<Permission> getUserPermissions(Project project, SafaUser currentUser) {

        Stream<Permission> permissions = projectMembershipService.getRolesForUser(currentUser, project)
            .stream()
            .flatMap(role -> role.getGrants().stream());

        Stream<Permission> teamPermissions =
            teamService.getUserPermissions(project.getOwningTeam(), currentUser).stream();

        return Stream.concat(permissions, teamPermissions).toList();
    }

    /**
     * Gets a project by its ID.
     *
     * @param id Project ID
     * @return The project
     */
    public Project getProjectById(UUID id) {
        return getProjectOptionalById(id)
            .orElseThrow(() -> new SafaItemNotFoundError("No project with the given ID found"));
    }

    /**
     * Gets a project by its ID. Returns an optional in case the project isn't found
     *
     * @param id Project ID
     * @return The project
     */
    public Optional<Project> getProjectOptionalById(UUID id) {
        return projectRepository.findById(id);
    }

    /**
     * Transfer ownership of a project to a new team
     * @param project The project to transfer
     * @param newTeam The team to transfer to
     * @return The updated project object
     */
    public Project transferProjectOwnership(Project project, Team newTeam) {
        assert project.getId() != null : "Cannot transfer ownership of a project which has not been saved.";
        assert newTeam.getId() != null : "Cannot transfer ownership of a project to a team which has not been saved";

        project.setOwningTeam(newTeam);
        return projectRepository.save(project);
    }
}
