package edu.nd.crc.safa.authentication.builders;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;
import edu.nd.crc.safa.features.organizations.services.TeamService;
import edu.nd.crc.safa.features.permissions.MissingPermissionException;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.features.versions.repositories.ProjectVersionRepository;

import lombok.AccessLevel;
import lombok.Getter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Responsible for fetching project and versions and asserting that
 * the current user has permissions to operate on it.
 */
@Component
public class ResourceBuilder {
    private final ProjectRepository projectRepository;
    private final ProjectVersionRepository projectVersionRepository;
    private final PermissionService permissionService;
    private final TeamService teamService;
    private final OrganizationService organizationService;

    @Autowired
    public ResourceBuilder(ProjectRepository projectRepository, ProjectVersionRepository projectVersionRepository,
                           PermissionService permissionService, TeamService teamService,
                           OrganizationService organizationService) {
        this.projectRepository = projectRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.permissionService = permissionService;
        this.teamService = teamService;
        this.organizationService = organizationService;
    }

    /**
     * Fetch a project by ID.
     *
     * @param projectId The ID of the project
     * @return The project in a holder that allows for easy permission checking
     * @throws SafaError If no project with that ID is found
     */
    public ObjectHolder<Project> fetchProject(UUID projectId) throws SafaError {
        Project project = this.projectRepository.findByProjectId(projectId);
        if (project == null) {
            throw new SafaItemNotFoundError("Unable to find project with ID: %s.", projectId);
        }
        return new ProjectHolder(project);
    }

    /**
     * Fetch a project version by ID.
     *
     * @param versionId The ID of the version.
     * @return The project version in a holder that allows for easy permission checking
     * @throws SafaError If no version with that ID is found
     */
    public ObjectHolder<ProjectVersion> fetchVersion(UUID versionId) throws SafaError {
        ProjectVersion projectVersion = this.projectVersionRepository.findByVersionId(versionId);
        if (projectVersion == null) {
            throw new SafaItemNotFoundError("Unable to find project version with id: %s.", versionId);
        }
        return new ProjectVersionHolder(projectVersion);
    }

    /**
     * Fetch a team by ID.
     *
     * @param teamId The ID of the team
     * @return The team in a holder that allows for easy permission checking
     */
    public ObjectHolder<Team> fetchTeam(UUID teamId) {
        return new TeamHolder(teamService.getTeamById(teamId));
    }

    /**
     * Fetch an organization by ID.
     *
     * @param organizationId The ID of the organization
     * @return The organization in a holder that allows for easy permission checking
     */
    public ObjectHolder<Organization> fetchOrganization(UUID organizationId) {
        return new OrganizationHolder(organizationService.getOrganizationById(organizationId));
    }

    /**
     * Specify a project so that we can check permissions on it
     *
     * @param project The project
     * @return A holder for the project
     */
    public ObjectHolder<Project> setProject(Project project) {
        return new ProjectHolder(project);
    }

    /**
     * An ObjectHolder is used to be able to quickly check permissions on objects
     *
     * @param <T> The type being held
     */
    public abstract static class ObjectHolder<T> {

        @Getter(AccessLevel.PROTECTED)
        private final T value;

        private Permission missingPermission;
        private boolean allowed = true;

        public ObjectHolder(T value) {
            this.value = value;
        }

        /**
         * Check the user has the given permission on the contained object.
         *
         * @param permission Permission to check
         * @param user The user to check permission for
         * @return This
         * @throws SafaError If the user doesn't have the permission
         */
        public ObjectHolder<T> withPermission(Permission permission, SafaUser user) throws SafaError {
            if (!hasPermission(permission, user)) {
                allowed = false;
                missingPermission = permission;
            }
            return this;
        }

        /**
         * Get the contained value
         *
         * @return The value
         */
        public T get() {
            if (!allowed) {
                throw new MissingPermissionException(missingPermission);
            }
            return value;
        }

        /**
         * Get the contained value only if all permission checks passed.
         * Otherwise, return an empty optional.
         *
         * @return The value if allowed, or an empty optional
         */
        public Optional<T> getOptional() {
            if (!allowed) {
                return Optional.empty();
            } else {
                return Optional.of(value);
            }
        }

        /**
         * Check that the user has a given permission for the held object and thrown an error if not.
         *
         * @param permission The permission to check
         * @param user The user to check for
         */
        protected abstract boolean hasPermission(Permission permission, SafaUser user) throws SafaError;
    }

    /**
     * Object holder for checking permissions on projects
     */
    private class ProjectHolder extends ObjectHolder<Project> {
        public ProjectHolder(Project project) {
            super(project);
        }

        @Override
        protected boolean hasPermission(Permission permission, SafaUser user) {
            return permissionService.hasPermission(permission, getValue(), user);
        }
    }

    /**
     * Object holder for checking permissions on projects while returning a specific version
     */
    private class ProjectVersionHolder extends ObjectHolder<ProjectVersion> {
        public ProjectVersionHolder(ProjectVersion projectVersion) {
            super(projectVersion);
        }

        @Override
        protected boolean hasPermission(Permission permission, SafaUser user) {
            return permissionService.hasPermission(permission, getValue().getProject(), user);
        }
    }

    /**
     * Object holder for checking permissions on teams
     */
    private class TeamHolder extends ObjectHolder<Team> {

        public TeamHolder(Team value) {
            super(value);
        }

        @Override
        protected boolean hasPermission(Permission permission, SafaUser user) throws SafaError {
            return permissionService.hasPermission(permission, getValue(), user);
        }
    }

    /**
     * Object holder for checking permissions on organizations
     */
    private class OrganizationHolder extends ObjectHolder<Organization> {

        public OrganizationHolder(Organization value) {
            super(value);
        }

        @Override
        protected boolean hasPermission(Permission permission, SafaUser user) throws SafaError {
            return permissionService.hasPermission(permission, getValue(), user);
        }
    }
}
