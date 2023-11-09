package edu.nd.crc.safa.authentication.builders;

import java.util.HashSet;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.permissions.MissingPermissionException;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AccessLevel;
import lombok.Getter;
import org.springframework.stereotype.Component;

/**
 * Responsible for fetching project and versions and asserting that
 * the current user has permissions to operate on it.
 */
@Component
public class ResourceBuilder {
    private final ServiceProvider serviceProvider;
    
    public ResourceBuilder() {
        serviceProvider = ServiceProvider.getInstance();
    }

    /**
     * Fetch a project by ID.
     *
     * @param projectId The ID of the project
     * @return The project in a holder that allows for easy permission checking
     * @throws SafaError If no project with that ID is found
     */
    public ObjectHolder<Project> fetchProject(UUID projectId) throws SafaError {
        Project project = serviceProvider.getProjectRepository().findByProjectId(projectId);
        if (project == null) {
            throw new SafaItemNotFoundError("Unable to find project with ID: %s.", projectId);
        }

        return membershipEntityHolder(project);
    }

    /**
     * Fetch a project version by ID.
     *
     * @param versionId The ID of the version.
     * @return The project version in a holder that allows for easy permission checking
     * @throws SafaError If no version with that ID is found
     */
    public ObjectHolder<ProjectVersion> fetchVersion(UUID versionId) throws SafaError {
        ProjectVersion projectVersion = serviceProvider.getProjectVersionRepository().findByVersionId(versionId);
        if (projectVersion == null) {
            throw new SafaItemNotFoundError("Unable to find project version with id: %s.", versionId);
        }

        return new ObjectHolder<>(projectVersion,
            (permission, user, value) -> getPermissionService().hasPermission(permission, value.getProject(), user)
        );
    }

    /**
     * Fetch a team by ID.
     *
     * @param teamId The ID of the team
     * @return The team in a holder that allows for easy permission checking
     */
    public ObjectHolder<Team> fetchTeam(UUID teamId) {
        Team team = serviceProvider.getTeamService().getTeamById(teamId);
        return membershipEntityHolder(team);
    }

    /**
     * Fetch an organization by ID.
     *
     * @param organizationId The ID of the organization
     * @return The organization in a holder that allows for easy permission checking
     */
    public ObjectHolder<Organization> fetchOrganization(UUID organizationId) {
        Organization organization = serviceProvider.getOrganizationService().getOrganizationById(organizationId);
        return membershipEntityHolder(organization);
    }

    /**
     * Fetch a document by ID
     *
     * @param documentId The ID of the document
     * @return The document in a holder that allows for easy permission checking
     */
    public ObjectHolder<Document> fetchDocument(UUID documentId) {
        Document document = serviceProvider.getDocumentService().getDocumentById(documentId);
        return new ObjectHolder<>(document,
            (permission, user, value) -> getPermissionService().hasPermission(permission, value.getProject(), user)
        );
    }

    /**
     * Utility function for creating object holders for entities that have memberships directly (rather
     * than simply referencing other objects that have memberships)
     *
     * @param value The entity
     * @param <T> The type of the entity
     * @return And object holder for the entity
     */
    private <T extends IEntityWithMembership> ObjectHolder<T> membershipEntityHolder(T value) {
        return new ObjectHolder<>(value,
            (permission, user, lambdaVal) -> getPermissionService().hasPermission(permission, lambdaVal, user)
        );
    }

    /**
     * Utility function to get the permission service to make lines shorter
     *
     * @return The permission service
     */
    private PermissionService getPermissionService() {
        return serviceProvider.getPermissionService();
    }

    /**
     * An ObjectHolder is used to be able to quickly check permissions on objects
     *
     * @param <T> The type being held
     */
    public static class ObjectHolder<T> {

        @Getter(AccessLevel.PROTECTED)
        private final T value;

        private final Set<Permission> missingPermissions = new HashSet<>();
        private boolean allowed = true;
        private final CheckPermissionFunction<T> hasPermissionFunction;

        private ObjectHolder(T value, CheckPermissionFunction<T> hasPermissionFunction) {
            this.value = value;
            this.hasPermissionFunction = hasPermissionFunction;
        }

        /**
         * Check the user has the given permission on the contained object.
         *
         * @param permission Permission to check
         * @param user       The user to check permission for
         * @return This
         * @throws SafaError If the user doesn't have the permission
         */
        public ObjectHolder<T> withPermission(Permission permission, SafaUser user) throws SafaError {
            if (!hasPermissionFunction.hasPermission(permission, user, getValue())) {
                allowed = false;
                missingPermissions.add(permission);
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
                throw new MissingPermissionException(missingPermissions, true);
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

    }

    /**
     * Functional interface for checking if a user has a permission associated with some object
     *
     * @param <T> The type of the object
     */
    @FunctionalInterface
    private interface CheckPermissionFunction<T> {
        /**
         * Check that the user has a given permission for the held object and thrown an error if not.
         *
         * @param permission The permission to check
         * @param user       The user to check for
         * @param value      The value of the object in the object holder
         */
        boolean hasPermission(Permission permission, SafaUser user, T value) throws SafaError;
    }

}
