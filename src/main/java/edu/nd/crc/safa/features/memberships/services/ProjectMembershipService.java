package edu.nd.crc.safa.features.memberships.services;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.memberships.entities.app.ProjectMemberAppEntity;
import edu.nd.crc.safa.features.memberships.entities.db.TeamProjectMembership;
import edu.nd.crc.safa.features.memberships.entities.db.UserProjectMembership;
import edu.nd.crc.safa.features.memberships.repositories.TeamProjectMembershipRepository;
import edu.nd.crc.safa.features.memberships.repositories.UserProjectMembershipRepository;
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
     */
    public void addUserRole(SafaUser user, Project project, ProjectRole role) {
        Optional<UserProjectMembership> membershipOptional =
                userProjectMembershipRepo.findByMemberAndProjectAndRole(user, project, role);

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

    /**
     * Returns list of projects owned or shared with current user.
     *
     * @param user The user to get projects for
     * @return List of projects where given user has access to.
     */
    public List<ProjectIdAppEntity> getProjectIdAppEntitiesForUser(SafaUser user) {
        return getProjectsForUser(user).stream()
                .map(project -> {
                    List<ProjectMemberAppEntity> members = this.userProjectMembershipRepo.findByProject(project)
                            .stream()
                            .map(ProjectMemberAppEntity::new)
                            .collect(Collectors.toList());
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
}
