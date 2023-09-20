package edu.nd.crc.safa.features.memberships.services;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.memberships.entities.db.TeamProjectMembership;
import edu.nd.crc.safa.features.memberships.entities.db.UserProjectMembership;
import edu.nd.crc.safa.features.memberships.repositories.TeamProjectMembershipRepository;
import edu.nd.crc.safa.features.memberships.repositories.UserProjectMembershipRepository;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.projects.entities.app.ProjectIdAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class ProjectMembershipService {

    private final ProjectService projectService;
    private final TeamProjectMembershipRepository teamProjectMembershipRepo;
    private final UserProjectMembershipRepository userProjectMembershipRepo;
    private final TeamMembershipService teamMembershipService;

    /**
     * Applies a role to a user within a project. If the user already has this
     * role in this project, this function does nothing.
     *
     * @param user The user to get the new role
     * @param project The project the role applies to
     * @param role The role
     * @return The new membership representing the role, or the old one if it already existed
     */
    public UserProjectMembership addUserRole(SafaUser user, Project project, ProjectRole role) {
        Optional<UserProjectMembership> membershipOptional =
                userProjectMembershipRepo.findByMemberAndProjectAndRole(user, project, role);

        if (membershipOptional.isEmpty()) {
            UserProjectMembership newMembership = new UserProjectMembership(project, user, role);
            return userProjectMembershipRepo.save(newMembership);
        } else {
            return membershipOptional.get();
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
                userProjectMembershipRepo.findByMemberAndProjectAndRole(user, project, role);

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
     * @return The new membership, or the old one if it already existed
     */
    public TeamProjectMembership addTeamToProject(Team team, Project project) {
        Optional<TeamProjectMembership> membershipOptional =
                teamProjectMembershipRepo.findByTeamAndProject(team, project);

        if (membershipOptional.isEmpty()) {
            TeamProjectMembership newMembership = new TeamProjectMembership(project, team);
            return teamProjectMembershipRepo.save(newMembership);
        } else {
            return membershipOptional.get();
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

    /**
     * Returns list of projects owned or shared with current user.
     *
     * @param user The user to get projects for
     * @return List of projects where given user has access to.
     */
    public List<ProjectIdAppEntity> getProjectIdAppEntitiesForUser(SafaUser user) {
        return getProjectsForUser(user).stream()
                .map(project -> {
                    List<MembershipAppEntity> members = this.userProjectMembershipRepo.findByProject(project)
                            .stream()
                            .map(MembershipAppEntity::new)
                            .collect(Collectors.toList());
                    this.teamMembershipService.getTeamMemberships(project.getOwningTeam())
                            .stream()
                            .map(MembershipAppEntity::new)
                            .forEach(members::add);
                    return new ProjectIdAppEntity(project, members);
                })
                .sorted(Comparator.comparing(ProjectIdAppEntity::getLastEdited).reversed())
                .collect(Collectors.toList());
    }

    /**
     * Returns list of projects owned or shared with the given user.
     *
     * @param user The user to get projects for
     * @return List of projects where the given user has access to.
     */
    public List<Project> getProjectsForUser(SafaUser user) {
        List<Project> projects = new ArrayList<>();

        this.userProjectMembershipRepo.findByMember(user)
                .stream()
                .map(UserProjectMembership::getProject)
                .forEach(projects::add);

        teamMembershipService.getUserTeams(user)
                .stream()
                .flatMap(team -> this.getProjectsForTeam(team).stream())
                .forEach(projects::add);

        return projects;
    }

    /**
     * Returns list of projects owned or shared with a team.
     *
     * @param team The team to get projects for
     * @return List of projects where the given team has access to.
     */
    public List<Project> getProjectsForTeam(Team team) {
        List<Project> projects = new ArrayList<>();

        this.teamProjectMembershipRepo.findByTeam(team)
                .stream()
                .map(TeamProjectMembership::getProject)
                .forEach(projects::add);

        projects.addAll(this.projectService.getProjectsOwnedByTeam(team));

        return projects;
    }

    /**
     * Returns the list of teams that have access to a project.
     *
     * @param project The project
     * @return The teams who can view the project
     */
    public List<TeamProjectMembership> getProjectTeams(Project project) {
        List<TeamProjectMembership> teamMemberships = this.teamProjectMembershipRepo.findByProject(project);
        teamMemberships.add(new TeamProjectMembership(project, project.getOwningTeam()));
        return teamMemberships;
    }

    /**
     * Returns list of members in given project for which the project was shared to them directly (rather than them
     * being on a team that has access).
     *
     * @param project The project whose members are retrieved.
     * @return List of project memberships relating members to projects.
     */
    public List<UserProjectMembership> getDirectProjectMembers(Project project) {
        return this.userProjectMembershipRepo.findByProject(project);
    }

    /**
     * Returns list of all users who are associated with a given project, either because it was shared with
     * them directly or they are on a team that has access.
     *
     * @param project The project whose members are retrieved.
     * @return List of project memberships relating members to projects.
     */
    public List<UserProjectMembership> getAllProjectMembers(Project project) {
        //TODO don't convert to user memberships
        List<UserProjectMembership> users = getDirectProjectMembers(project);
        List<TeamProjectMembership> teams = getProjectTeams(project);

        Set<SafaUser> seenUsers = new HashSet<>();
        users.stream()
                .map(UserProjectMembership::getMember)
                .forEach(seenUsers::add);

        teams.stream()
                .map(TeamProjectMembership::getTeam)
                .flatMap(team -> teamMembershipService.getUsersInTeam(team).stream())
                .forEach(user -> {
                    if (!seenUsers.contains(user)) {
                        users.add(new UserProjectMembership(project, user, ProjectRole.NONE));
                        seenUsers.add(user);
                    }
                });

        return users;
    }
}
