package edu.nd.crc.safa.authentication.builders;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;
import java.util.function.Function;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.permissions.MissingPermissionException;
import edu.nd.crc.safa.features.permissions.checks.AdditionalPermissionCheck;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

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
    private final ServiceProvider serviceProvider;

    @Autowired
    public ResourceBuilder(ServiceProvider serviceProvider) {
        this.serviceProvider = serviceProvider;
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

        return membershipEntityHolder(projectVersion);
    }

    /**
     * Sets project version as entity.
     *
     * @param projectVersion The project version to set.
     * @return Object holder with project version.
     */
    public ObjectHolder<ProjectVersion> withVersion(ProjectVersion projectVersion) {
        return membershipEntityHolder(projectVersion);
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
        return entityWithProjectHolder(document, Document::getProject);
    }

    /**
     * Fetch a type by ID
     *
     * @param typeId The ID of the type
     * @return The type in a holder that allows for easy permission checking
     */
    public ObjectHolder<ArtifactType> fetchType(UUID typeId) {
        ArtifactType type = serviceProvider.getTypeService().getArtifactType(typeId);
        if (type == null) {
            throw new SafaItemNotFoundError("No type with id %s", typeId);
        }

        return entityWithProjectHolder(type, ArtifactType::getProject);
    }

    /**
     * Fetch an artifact by ID
     *
     * @param artifactId The ID of the artifact
     * @return The artifact in a holder that allows for easy permission checking
     */
    public ObjectHolder<Artifact> fetchArtifact(UUID artifactId) {
        Artifact artifact = serviceProvider.getArtifactRepository().findById(artifactId)
            .orElseThrow(() -> new SafaItemNotFoundError("No artifact with ID %s found", artifactId));
        return entityWithProjectHolder(artifact, Artifact::getProject);
    }

    /**
     * Utility function for creating object holders for entities that have memberships directly (rather
     * than simply referencing other objects that have memberships)
     *
     * @param value The entity
     * @param <T>   The type of the entity
     * @return An object holder for the entity
     */
    private <T extends IEntityWithMembership> ObjectHolder<T> membershipEntityHolder(T value) {
        return new ObjectHolder<>(value,
            (permissions, user, lambdaVal) -> getPermissionService().hasPermissions(permissions, lambdaVal, user),
            (permissions, user, lambdaVal) -> getPermissionService().hasAnyPermission(permissions, lambdaVal, user),
            (check, user, lambdaVal) -> getPermissionService().hasAdditionalCheck(check, lambdaVal, user));
    }

    /**
     * Utility function for creating object holders for entities that can easily be linked to a project
     *
     * @param value            The entity
     * @param projectRetriever A function that allows us to get the project for this entity
     * @param <T>              The type of the entity
     * @return An object holder for the entity
     */
    private <T> ObjectHolder<T> entityWithProjectHolder(T value, Function<T, Project> projectRetriever) {
        return new ObjectHolder<>(value,
            (permissions, user, lambdaVal) ->
                getPermissionService().hasPermissions(permissions, projectRetriever.apply(lambdaVal), user),
            (permissions, user, lambdaVal) ->
                getPermissionService().hasAnyPermission(permissions, projectRetriever.apply(lambdaVal), user),
            (check, user, lambdaVal) ->
                getPermissionService().hasAdditionalCheck(check, projectRetriever.apply(lambdaVal), user));
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
     * Functional interface for checking if a user has a permission associated with some object
     *
     * @param <T> The type of the object
     */
    @FunctionalInterface
    private interface CheckPermissionFunction<T> {
        /**
         * Check that the user has given permissions for the held object and thrown an error if not.
         *
         * @param permissions The permissions to check
         * @param user        The user to check for
         * @param value       The value of the object in the object holder
         */
        boolean apply(Set<Permission> permissions, SafaUser user, T value) throws SafaError;
    }

    /**
     * Functional interface for checking if a user has an {@link AdditionalPermissionCheck} associated with some object
     *
     * @param <T> The type of the object
     */
    @FunctionalInterface
    private interface CheckAdditionalCheckFunction<T> {
        /**
         * Check that the user has a given additional check for the held object and thrown an error if not.
         *
         * @param check The thing to check
         * @param user  The user to check for
         * @param value The value of the object in the object holder
         */
        boolean apply(AdditionalPermissionCheck check, SafaUser user, T value) throws SafaError;
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
        private final List<String> failedAdditionalChecks = new ArrayList<>();
        private final CheckPermissionFunction<T> hasPermissionFunction;
        private final CheckPermissionFunction<T> hasAnyPermissionFunction;
        private final CheckAdditionalCheckFunction<T> hasAdditionalCheckFunction;
        private boolean allowed = true;
        private SafaUser checkUser = null;

        private ObjectHolder(T value,
                             CheckPermissionFunction<T> hasPermissionFunction,
                             CheckPermissionFunction<T> hasAnyPermissionFunction,
                             CheckAdditionalCheckFunction<T> hasAdditionalCheckFunction) {
            this.value = value;
            this.hasPermissionFunction = hasPermissionFunction;
            this.hasAnyPermissionFunction = hasAnyPermissionFunction;
            this.hasAdditionalCheckFunction = hasAdditionalCheckFunction;
        }

        /**
         * Sets the user that checks will be performed against
         *
         * @param user The user to check
         * @return This
         */
        public ObjectHolder<T> asUser(SafaUser user) {
            checkUser = user;
            return this;
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
            if (!hasPermissionFunction.apply(Set.of(permission), user, getValue())) {
                allowed = false;
                missingPermissions.add(permission);
            }
            return this;
        }

        /**
         * Check the user has the given permission on the contained object.
         * Requires that {@link #asUser(SafaUser)} was called first
         *
         * @param permission Permission to check
         * @return This
         * @throws SafaError If the user doesn't have the permission
         */
        public ObjectHolder<T> withPermission(Permission permission) throws SafaError {
            assert checkUser != null : "asUser must be called before this function";
            return withPermission(permission, checkUser);
        }

        /**
         * Check the user has the given permissions on the contained object.
         *
         * @param permissions Permissions to check
         * @param user        The user to check permission for
         * @return This
         * @throws SafaError If the user doesn't have the permission
         */
        public ObjectHolder<T> withPermissions(Set<Permission> permissions, SafaUser user) throws SafaError {
            if (!hasPermissionFunction.apply(permissions, user, getValue())) {
                allowed = false;
                missingPermissions.addAll(permissions);
            }
            return this;
        }

        /**
         * Check the user has the given permissions on the contained object.
         * Requires that {@link #asUser(SafaUser)} was called first
         *
         * @param permissions Permissions to check
         * @return This
         * @throws SafaError If the user doesn't have the permission
         */
        public ObjectHolder<T> withPermissions(Set<Permission> permissions) throws SafaError {
            assert checkUser != null : "asUser must be called before this function";
            return withPermissions(permissions, checkUser);
        }

        /**
         * Check the user has the given permissions on the contained object.
         *
         * @param permissions Permissions to check
         * @param user        The user to check permissions for
         * @return This
         * @throws SafaError If the user doesn't have the permissions
         */
        public ObjectHolder<T> withAnyPermission(Set<Permission> permissions, SafaUser user) throws SafaError {
            if (!hasAnyPermissionFunction.apply(permissions, user, getValue())) {
                allowed = false;
                missingPermissions.addAll(permissions);
            }
            return this;
        }

        /**
         * Check the user has the given permissions on the contained object.
         * Requires that {@link #asUser(SafaUser)} was called first
         *
         * @param permissions Permissions to check
         * @return This
         * @throws SafaError If the user doesn't have the permissions
         */
        public ObjectHolder<T> withAnyPermission(Set<Permission> permissions) throws SafaError {
            assert checkUser != null : "asUser must be called before this function";
            return withAnyPermission(permissions, checkUser);
        }

        /**
         * Check the check object passes for the given user
         *
         * @param check The thing to check
         * @param user  The user to check for
         * @return This
         * @throws SafaError If the user doesn't have the permissions
         */
        public ObjectHolder<T> withAdditionalCheck(AdditionalPermissionCheck check, SafaUser user) throws SafaError {
            if (!hasAdditionalCheckFunction.apply(check, user, getValue())) {
                allowed = false;
                failedAdditionalChecks.add(check.getMessage());
            }
            return this;
        }

        /**
         * Check the check object passes for the given user. Requires that {@link #asUser(SafaUser)} was called first
         *
         * @param check The thing to check
         * @return This
         * @throws SafaError If the user doesn't have the permissions
         */
        public ObjectHolder<T> withAdditionalCheck(AdditionalPermissionCheck check) throws SafaError {
            assert checkUser != null : "asUser must be called before this function";
            return withAdditionalCheck(check, checkUser);
        }

        /**
         * Get the contained value
         *
         * @return The value
         */
        public T get() {
            if (!allowed) {
                throw new MissingPermissionException(missingPermissions, true, failedAdditionalChecks);
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

}
