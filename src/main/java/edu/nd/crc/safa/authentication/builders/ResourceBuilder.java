package edu.nd.crc.safa.authentication.builders;

import java.util.UUID;

import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.features.versions.repositories.ProjectVersionRepository;

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

    @Autowired
    public ResourceBuilder(ProjectRepository projectRepository,
                           ProjectVersionRepository projectVersionRepository,
                           PermissionService permissionService) {
        this.projectRepository = projectRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.permissionService = permissionService;
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
            throw new SafaError("Unable to find project with ID: %s.", projectId);
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
            throw new SafaError("Unable to find project version with id: %s.", versionId);
        }
        return new ProjectVersionHolder(projectVersion);
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

        protected T value;

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
            this.requirePermission(permission, user);
            return this;
        }

        /**
         * Get the contained value
         *
         * @return The value
         */
        public T get() {
            return value;
        }

        /**
         * Check that the user has a given permission for the held object and thrown an error if not.
         *
         * @param permission The permission to check
         * @param user The user to check for
         */
        protected abstract void requirePermission(Permission permission, SafaUser user) throws SafaError;
    }

    private class ProjectHolder extends ObjectHolder<Project> {
        public ProjectHolder(Project project) {
            super(project);
        }

        @Override
        protected void requirePermission(Permission permission, SafaUser user) {
            permissionService.requirePermission(permission, value, user);
        }
    }

    private class ProjectVersionHolder extends ObjectHolder<ProjectVersion> {
        public ProjectVersionHolder(ProjectVersion projectVersion) {
            super(projectVersion);
        }

        @Override
        protected void requirePermission(Permission permission, SafaUser user) {
            permissionService.requirePermission(permission, value.getProject(), user);
        }
    }
}
