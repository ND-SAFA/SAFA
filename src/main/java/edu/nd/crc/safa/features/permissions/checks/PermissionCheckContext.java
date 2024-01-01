package edu.nd.crc.safa.features.permissions.checks;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.Getter;

/**
 * <p>Class containing context information for a permission check. This
 * facilitates permissions having extra checks.</p>
 * <br/>
 * <p>Use the static {@code builder()} method to build a new context</p>
 */
@Getter
public class PermissionCheckContext {
    private Organization organization;
    private Team team;
    private Project project;
    private ProjectVersion projectVersion;
    private SafaUser user;
    private ServiceProvider serviceProvider;

    public static PermissionCheckContextBuilder builder() {
        return new PermissionCheckContextBuilder();
    }

    /**
     * Builder for {@link PermissionCheckContext}
     */
    public static class PermissionCheckContextBuilder {
        private final PermissionCheckContext context;

        private PermissionCheckContextBuilder() {
            this.context = new PermissionCheckContext();
        }

        /**
         * Add the service provider to the context
         *
         * @param serviceProvider The service provider
         * @return The builder
         */
        public PermissionCheckContextBuilder add(ServiceProvider serviceProvider) {
            context.serviceProvider = serviceProvider;
            return this;
        }

        /**
         * Add a user to the context
         *
         * @param user The user
         * @return The builder
         */
        public PermissionCheckContextBuilder add(SafaUser user) {
            context.user = user;
            return this;
        }

        /**
         * Add an organization to the context
         *
         * @param organization The organization
         * @return The builder
         */
        public PermissionCheckContextBuilder add(Organization organization) {
            context.organization = organization;
            context.team = null;
            context.project = null;
            context.projectVersion = null;
            return this;
        }

        /**
         * Add a team to the context. This also implicitly adds
         * the organization.
         *
         * @param team The team
         * @return The builder
         */
        public PermissionCheckContextBuilder add(Team team) {
            context.organization = team.getOrganization();
            context.team = team;
            context.project = null;
            context.projectVersion = null;
            return this;
        }

        /**
         * Add a project to the context. This also implicitly adds
         * the team and organization associated with the project.
         *
         * @param project The project
         * @return The builder
         */
        public PermissionCheckContextBuilder add(Project project) {
            context.organization = project.getOwningTeam().getOrganization();
            context.team = project.getOwningTeam();
            context.project = project;
            context.projectVersion = null;
            return this;
        }

        /**
         * Add a project version to the context. This also implicitly adds
         * the team, organization, and project associated with the project version.
         *
         * @param projectVersion The project version
         * @return The builder
         */
        public PermissionCheckContextBuilder add(ProjectVersion projectVersion) {
            context.organization = projectVersion.getProject().getOwningTeam().getOrganization();
            context.team = projectVersion.getProject().getOwningTeam();
            context.project = projectVersion.getProject();
            context.projectVersion = projectVersion;
            return this;
        }

        /**
         * Add a membership entity to the context. This will determine
         * the object's actual type and call the appropriate overload.
         *
         * @param entity The entity
         * @return The builder
         */
        public PermissionCheckContextBuilder add(IEntityWithMembership entity) {
            if (entity instanceof Organization) {
                add((Organization) entity);
            } else if (entity instanceof Team) {
                add((Team) entity);
            } else if (entity instanceof Project) {
                add((Project) entity);
            } else if (entity instanceof ProjectVersion) {
                add((ProjectVersion) entity);
            } else {
                throw new IllegalArgumentException("Unknown type: " + entity.getClass());
            }
            return this;
        }

        /**
         * Get the created context
         *
         * @return The context
         */
        public PermissionCheckContext get() {
            return context;
        }
    }
}
