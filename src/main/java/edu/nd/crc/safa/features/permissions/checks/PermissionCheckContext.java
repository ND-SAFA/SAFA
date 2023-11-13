package edu.nd.crc.safa.features.permissions.entities;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Getter;

/**
 * Class containing context information for a permission check. This
 * facilitates permissions having extra checks.
 */
@Getter
public class PermissionCheckContext {
    private Organization organization;
    private Team team;
    private Project project;
    private SafaUser user;
    private ServiceProvider serviceProvider;

    /**
     * Add the service provider to the context
     *
     * @param serviceProvider The service provider
     */
    public void add(ServiceProvider serviceProvider) {
        this.serviceProvider = serviceProvider;
    }

    /**
     * Add a user to the context
     *
     * @param user The user
     */
    public void add(SafaUser user) {
        this.user = user;
    }

    /**
     * Add an organization to the context
     *
     * @param organization The organization
     */
    public void add(Organization organization) {
        this.organization = organization;
    }

    /**
     * Add a team to the context. This also implicitly adds
     * the organization.
     *
     * @param team The team
     */
    public void add(Team team) {
        this.team = team;
        add(team.getOrganization());
    }

    /**
     * Add a project to the context. This also implicitly adds
     * the team and organization associated with the project.
     *
     * @param project The project
     */
    public void add(Project project) {
        this.project = project;
        add(project.getOwningTeam());
    }

    /**
     * Add a membership entity to the context. This will determine
     * the object's actual type and call the appropriate overload.
     *
     * @param entity The entity
     */
    public void add(IEntityWithMembership entity) {
        if (entity instanceof Organization) {
            add((Organization) entity);
        } else if (entity instanceof Team) {
            add((Team) entity);
        } else if (entity instanceof Project) {
            add((Project) entity);
        } else {
            throw new IllegalArgumentException("Unknown type: " + entity.getClass());
        }
    }
}
