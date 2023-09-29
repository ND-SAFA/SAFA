package edu.nd.crc.safa.features.projects.services;

import java.io.IOException;
import java.util.Collection;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import edu.nd.crc.safa.config.ProjectPaths;
<<<<<<< HEAD
import edu.nd.crc.safa.features.memberships.entities.db.ProjectMembership;
import edu.nd.crc.safa.features.memberships.services.ProjectMembershipService;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
=======
import edu.nd.crc.safa.features.jobs.services.JobService;
>>>>>>> 5ac3d9f1a3c5731843e4d7383f54789aed7695a7
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.services.TeamService;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
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

    @Setter(onMethod = @__({@Autowired}))
    private JobService jobService;

    /**
     * Deletes given project and all related entities through cascade property.
     *
     * @param project The project to delete.
     * @throws SafaError Throws error if error occurs while deleting flat files.
     */
    public void deleteProject(Project project) throws SafaError, IOException {
        this.jobService.removeProjectFromJobs(project);
        this.projectRepository.delete(project);
        FileUtilities.deletePath(ProjectPaths.Storage.projectPath(project, false));
    }

    /**
     * Creates a new project
     *
     * @param name The name of the project
     * @param description The description of the project
     * @param owner The team that owns the project
     * @return The new project
     */
    public Project createProject(String name, String description, Team owner) {
        Project project = new Project(name, description, owner);
        return this.projectRepository.save(project);
    }

    /**
     * Creates a new project
     *
     * @param name The name of the project
     * @param description The description of the project
     * @param owner The user that owns the project
     * @return The new project
     */
    public Project createProject(String name, String description, SafaUser owner) {
        Team personalTeam = teamService.getPersonalTeam(owner);
        return createProject(name, description, personalTeam);
    }

    /**
     * Creates a new project
     *
     * @param name The name of the project
     * @param description The description of the project
     * @param owner The organization that owns the project
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
     * @param owner The user who will own the project
     * @return The new project
     */
    public Project createProject(ProjectAppEntity projectDefinition, SafaUser owner) {
        return createProject(projectDefinition.getName(), projectDefinition.getDescription(), owner);
    }

    /**
     * Creates a new project
     *
     * @param projectDefinition The definition of the project from the front end
     * @param owner The organization who will own the project
     * @return The new project
     */
    public Project createProject(ProjectAppEntity projectDefinition, Organization owner) {
        return createProject(projectDefinition.getName(), projectDefinition.getDescription(), owner);
    }

    /**
     * Creates a new project
     *
     * @param projectDefinition The definition of the project from the front end
     * @param owner The team who will own the project
     * @return The new project
     */
    public Project createProject(ProjectAppEntity projectDefinition, Team owner) {
        return createProject(projectDefinition.getName(), projectDefinition.getDescription(), owner);
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
     * @param project The project
     * @param currentUser The user making the request (so that we can properly show permissions)
     * @return The project identifier
     */
    public ProjectIdAppEntity getIdAppEntity(Project project, SafaUser currentUser) {
        List<ProjectMembership> projectMemberships =
            projectMembershipService.getProjectMembers(project);

        List<MembershipAppEntity> membershipAppEntities =
            projectMemberships
                .stream()
                .map(MembershipAppEntity::new)
                .collect(Collectors.toUnmodifiableList());

        List<String> permissions = getUserPermissions(project, currentUser)
            .stream()
            .filter(permission -> permission instanceof ProjectPermission)
            .map(Permission::getName)
            .collect(Collectors.toUnmodifiableList());

        return new ProjectIdAppEntity(project, membershipAppEntities, permissions);
    }

    /**
     * Converts a collection of projects to project identifiers
     *
     * @param projects The projects
     * @param currentUser The user making the request (so that we can properly show permissions)
     * @return A list of project identifier objects
     */
    public List<ProjectIdAppEntity> getIdAppEntities(Collection<Project> projects, SafaUser currentUser) {
        return projects.stream()
            .map(project -> getIdAppEntity(project, currentUser))
            .collect(Collectors.toUnmodifiableList());
    }

    /**
     * Get all permissions granted to the user via their membership(s) within the given team.
     *
     * @param project The project the user is a part of. Note that the user can have permissions on a project even if
     *                they do not have a direct project membership, as they could be a member of a team or an
     *                organization that grants them project permissions.
     * @param currentUser The user in question
     * @return A list of permissions the user has for the project
     */
    public List<Permission> getUserPermissions(Project project, SafaUser currentUser) {

        Stream<Permission> permissions = projectMembershipService.getUserRoles(currentUser, project)
            .stream()
            .flatMap(role -> role.getGrants().stream());

        Stream<Permission> teamPermissions =
            teamService.getUserPermissions(project.getOwningTeam(), currentUser).stream();

        return Stream.concat(permissions, teamPermissions).collect(Collectors.toUnmodifiableList());
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
}
