package edu.nd.crc.safa.features.memberships.services;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.memberships.entities.db.TeamProjectMembership;
import edu.nd.crc.safa.features.memberships.entities.db.UserProjectMembership;
import edu.nd.crc.safa.features.memberships.repositories.TeamProjectMembershipRepository;
import edu.nd.crc.safa.features.memberships.repositories.UserProjectMembershipRepository;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class ProjectMembershipService {

    private final TeamProjectMembershipRepository teamProjectMembershipRepo;
    private final UserProjectMembershipRepository userProjectMembershipRepo;

    /**
     * Applies a role to a user within a project. If the user already has this
     * role in this project, this function does nothing.
     *
     * @param user The user to get the new role
     * @param project The project the role applies to
     * @param role The role
     */
    public void addUserRole(SafaUser user, Project project, ProjectRole role) {
        Optional<UserProjectMembership> membershipOptional =
                userProjectMembershipRepo.findByUserAndProjectAndRole(user, project, role);

        if (membershipOptional.isEmpty()) {
            UserProjectMembership newMembership = new UserProjectMembership(project, user, role);
            userProjectMembershipRepo.save(newMembership);
        }
    }

    /**
     * Removes a role from a user within a project. If the user didn't already have this
     * role in this project, this function does nothing.
     *
     * @param user The user to remove the role from
     * @param project The project the role applies to
     * @param role The role
     */
    public void removeUserRole(SafaUser user, Project project, ProjectRole role) {
        Optional<UserProjectMembership> membershipOptional =
                userProjectMembershipRepo.findByUserAndProjectAndRole(user, project, role);

        membershipOptional.ifPresent(userProjectMembershipRepo::delete);
    }

    /**
     * Get the list of roles the user has within the project.
     *
     * @param user The user in question
     * @param project The project to check within
     * @return The roles the user has in that project
     */
    public List<ProjectRole> getUserRoles(SafaUser user, Project project) {
        return userProjectMembershipRepo.findByProjectAndMember(project, user).stream()
                .map(UserProjectMembership::getRole)
                .collect(Collectors.toUnmodifiableList());
    }

    /**
     * Share a project with a team. The new team with be able to view the project in read-only mode.
     *
     * @param team The team to share the project with.
     * @param project The project to share.
     */
    public void addTeamToProject(Team team, Project project) {
        Optional<TeamProjectMembership> membershipOptional =
                teamProjectMembershipRepo.findByTeamAndProject(team, project);

        if (membershipOptional.isEmpty()) {
            TeamProjectMembership newMembership = new TeamProjectMembership(project, team);
            teamProjectMembershipRepo.save(newMembership);
        }
    }

    /**
     * Remove a team from a project. Members of the team won't be able to see the project anymore
     * unless they are associated with the project via another team.
     *
     * @param team The team to remove from the project.
     * @param project The project to remove the team from.
     */
    public void removeTeamFromProject(Team team, Project project) {
        if (team.equals(project.getOwningTeam())) {
            throw new IllegalArgumentException("Cannot remove the team that owns the project.");
        }

        Optional<TeamProjectMembership> membershipOptional =
                teamProjectMembershipRepo.findByTeamAndProject(team, project);

        membershipOptional.ifPresent(teamProjectMembershipRepo::delete);
    }
}
