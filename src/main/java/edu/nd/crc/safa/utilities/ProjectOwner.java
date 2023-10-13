package edu.nd.crc.safa.utilities;

import java.util.UUID;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Data;

/**
 * Holder for a project owner which is used so that we can have all of the logic in a common function.
 */
@Data
public class ProjectOwner {
    private Organization organization;
    private Team team;
    private SafaUser user;

    public ProjectOwner(Organization organization) {
        this.organization = organization;
    }

    public ProjectOwner(Team team) {
        this.team = team;
    }

    public ProjectOwner(SafaUser user) {
        this.user = user;
    }

    /**
     * Utility function to create a project owner object. Provide a team ID, an org ID, or neither,
     * and it will get the appropriate project owner entity and construct a project owner object from it.
     * <br>
     * Team ID takes precedence over org ID, and if neither are provided, the current user is used.
     *
     * @param serviceProvider Service provider so that we can retrieve teams and orgs
     * @param teamId          Optional ID of the team that will own the project
     * @param orgId           Optional ID of the organization that will own the project
     * @param user            The user to default to if the uuids are null
     * @return A project owner object created using the above rules
     */
    public static ProjectOwner fromUUIDs(ServiceProvider serviceProvider,
                                         UUID teamId, UUID orgId, SafaUser user) {
        if (teamId != null) {
            Team team = serviceProvider.getTeamService().getTeamById(teamId);
            return new ProjectOwner(team);
        } else if (orgId != null) {
            Organization org = serviceProvider.getOrganizationService().getOrganizationById(orgId);
            return new ProjectOwner(org);
        } else {
            return new ProjectOwner(user);
        }
    }
}
