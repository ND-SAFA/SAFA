package edu.nd.crc.safa.features.memberships.services;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.memberships.entities.db.TeamMembership;
import edu.nd.crc.safa.features.memberships.repositories.TeamMembershipRepository;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipType;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.entities.db.TeamRole;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
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
     * @return The new team membership, or the old one if it already existed
     */
    public TeamMembership addUserRole(SafaUser user, Team team, TeamRole role) {
        Optional<TeamMembership> membershipOptional =
            teamMembershipRepo.findByUserAndTeamAndRole(user, team, role);

        return membershipOptional.orElseGet(() -> {
            TeamMembership newMembership = new TeamMembership(user, team, role);
            return teamMembershipRepo.save(newMembership);
        });
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

    /**
     * Get all teams for a user.
     *
     * @param user The user
     * @return The teams the user is on
     */
    public List<Team> getUserTeams(SafaUser user) {
        return teamMembershipRepo.findByUser(user)
            .stream()
            .map(TeamMembership::getTeam)
            .collect(Collectors.toList());
    }

    /**
     * Get all team membership objects associated with a team
     *
     * @param team The team
     * @return The team memberships in that team
     */
    public List<TeamMembership> getTeamMemberships(Team team) {
        return teamMembershipRepo.findByTeam(team);
    }

    /**
     * Get all users within a team
     *
     * @param team The team
     * @return The members of the team
     */
    public List<SafaUser> getUsersInTeam(Team team) {
        return getTeamMemberships(team)
            .stream()
            .map(TeamMembership::getUser)
            .distinct()
            .collect(Collectors.toUnmodifiableList());
    }

    /**
     * Search for a team membership by its ID.
     *
     * @param membershipId The ID of the membership
     * @return The membership, if it exists
     */
    public Optional<TeamMembership> getMembershipOptionalById(UUID membershipId) {
        return teamMembershipRepo.findById(membershipId);
    }

    /**
     * Search for a team membership by its ID. Throw an exception
     * if it's not found.
     *
     * @param membershipId The ID of the membership
     * @return The membership, if it exists
     * @throws SafaItemNotFoundError If the membership could not be found
     */
    public TeamMembership getMembershipById(UUID membershipId) {
        return getMembershipOptionalById(membershipId)
            .orElseThrow(() -> new SafaItemNotFoundError("No membership found with the specified ID"));
    }

    /**
     * Returns the team members of the project.
     *
     * @param project Project whose members are returned.
     * @return List of team members with access to the project.
     */
    public List<MembershipAppEntity> getProjectMemberships(Project project) {
        Team owningTeam = project.getOwningTeam();
        List<TeamMembership> teamMembers = this.getTeamMemberships(owningTeam);
        return teamMembers
            .stream()
            .map(m -> {
                MembershipAppEntity membershipAppEntity = new MembershipAppEntity();
                membershipAppEntity.setEntityType(MembershipType.TEAM);
                membershipAppEntity.setEntityId(owningTeam.getId());
                membershipAppEntity.setEmail(m.getEmail());
                membershipAppEntity.setRole(m.getRoleAsString());
                return membershipAppEntity;
            }).collect(Collectors.toList());
    }
}
