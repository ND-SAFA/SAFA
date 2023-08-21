package edu.nd.crc.safa.features.memberships.services;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.memberships.entities.db.TeamMembership;
import edu.nd.crc.safa.features.memberships.repositories.TeamMembershipRepository;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.entities.db.TeamRole;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class TeamMembershipService {

    private final TeamMembershipRepository teamMembershipRepo;

    /**
     * Applies a role to a user within a team. If the user already has this
     * role in this team, this function does nothing.
     *
     * @param user The user to get the new role
     * @param team The team the role applies to
     * @param role The role
     */
    public void addUserRole(SafaUser user, Team team, TeamRole role) {
        Optional<TeamMembership> membershipOptional =
                teamMembershipRepo.findByUserAndTeamAndRole(user, team, role);

        if (membershipOptional.isEmpty()) {
            TeamMembership newMembership = new TeamMembership(user, team, role);
            teamMembershipRepo.save(newMembership);
        }
    }

    /**
     * Removes a role from a user within a team. If the user didn't already have this
     * role in this team, this function does nothing.
     *
     * @param user The user to remove the role from
     * @param team The team the role applies to
     * @param role The role
     */
    public void removeUserRole(SafaUser user, Team team, TeamRole role) {
        Optional<TeamMembership> membershipOptional =
                teamMembershipRepo.findByUserAndTeamAndRole(user, team, role);

        membershipOptional.ifPresent(teamMembershipRepo::delete);
    }

    /**
     * Get the list of roles the user has within the team.
     *
     * @param user The user in question
     * @param team The team to check within
     * @return The roles the user has in that team
     */
    public List<TeamRole> getUserRoles(SafaUser user, Team team) {
        return teamMembershipRepo.findByUserAndTeam(user, team).stream()
                .map(TeamMembership::getRole)
                .collect(Collectors.toUnmodifiableList());
    }
}
