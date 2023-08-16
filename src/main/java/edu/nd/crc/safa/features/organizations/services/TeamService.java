package edu.nd.crc.safa.features.organizations.services;

import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.repositories.TeamRepository;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class TeamService {

    private final TeamRepository teamRepo;

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
}
