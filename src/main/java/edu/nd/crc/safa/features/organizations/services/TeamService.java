package edu.nd.crc.safa.features.organizations.services;

import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.repositories.TeamRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Setter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Service;

@Service
public class TeamService {

    @Setter(onMethod = @__({@Autowired}))
    private TeamRepository teamRepo;

    @Setter(onMethod = @__({@Autowired, @Lazy}))
    private OrganizationService orgService;

    /**
     * Create a new team.
     *
     * @param name The name of the team
     * @param organization The organization the team belongs to
     * @param fullOrgTeam Whether the team is a full organization team
     * @return The newly created team
     */
    public Team createNewTeam(String name, Organization organization, boolean fullOrgTeam) {
        Team team = new Team(name, organization, fullOrgTeam);
        return teamRepo.save(team);
    }

    /**
     * Gets the team associated with the user's personal org
     *
     * @param user The user
     * @return The user's personal team
     */
    public Team getPersonalTeam(SafaUser user) {
        Organization personalOrg = orgService.getPersonalOrganization(user);
        return getFullOrganizationTeam(personalOrg);
    }

    /**
     * Gets the team that contains the entire organization
     *
     * @param organization The organization
     * @return The full organization team
     */
    public Team getFullOrganizationTeam(Organization organization) {
        UUID teamId = organization.getFullOrgTeamId();
        return teamRepo.findById(teamId).orElseThrow(() -> new SafaError("Organization does not have an org team"));
    }
}
