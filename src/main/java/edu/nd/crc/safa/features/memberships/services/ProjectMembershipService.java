package edu.nd.crc.safa.features.memberships.services;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.memberships.entities.db.ProjectMembership;
import edu.nd.crc.safa.features.memberships.repositories.UserProjectMembershipRepository;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.projects.entities.app.ProjectIdAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class ProjectMembershipService {

    private final ProjectService projectService;
    private final UserProjectMembershipRepository userProjectMembershipRepo;
    private final TeamMembershipService teamMembershipService;
    private final NotificationService notificationService;

    /**
     * Applies a role to a user within a project. If the user already has this
     * role in this project, this function does nothing.
     *
     * @param user    The user to get the new role
     * @param project The project the role applies to
     * @param role    The role
     * @return The new membership representing the role, or the old one if it already existed
     */
    public ProjectMembership addUserRole(SafaUser user, Project project, ProjectRole role) {
        Optional<ProjectMembership> membershipOptional =
            userProjectMembershipRepo.findByMemberAndProjectAndRole(user, project, role);

        ProjectMembership membership = membershipOptional.orElseGet(() -> {
            ProjectMembership newMembership = new ProjectMembership(project, user, role);
            return userProjectMembershipRepo.save(newMembership);
        });

        notificationService.broadcastChange(
            EntityChangeBuilder
                .create(user, project)
                .withMembersUpdate(membership.getId())
        );

        notificationService.broadcastChange(
            EntityChangeBuilder.create(user)
                .withProjectUpdate(project)
        );

        return membership;
    }

    /**
     * Removes a role from a user within a project. If the user didn't already have this
     * role in this project, this function does nothing.
     *
     * @param user    The user to remove the role from
     * @param project The project the role applies to
     * @param role    The user's role in the project.
     */
    public void removeUserRole(SafaUser user, Project project, ProjectRole role) {
        Optional<ProjectMembership> membershipOptional =
            userProjectMembershipRepo.findByMemberAndProjectAndRole(user, project, role);

        if (membershipOptional.isPresent()) {
            userProjectMembershipRepo.delete(membershipOptional.get());

            notificationService.broadcastChange(
                EntityChangeBuilder.create(user, project)
                    .withMembersDelete(membershipOptional.get().getId())
            );
        }
    }

    /**
     * Get the list of roles the user has within the project.
     *
     * @param user    The user in question
     * @param project The project to check within
     * @return The roles the user has in that project
     */
    public List<ProjectRole> getUserRoles(SafaUser user, Project project) {
        return userProjectMembershipRepo.findByProjectAndMember(project, user).stream()
            .map(ProjectMembership::getRole)
            .collect(Collectors.toUnmodifiableList());
    }

    /**
     * Returns list of projects owned or shared with current user.
     *
     * @param user The user to get projects for
     * @return List of projects where given user has access to.
     */
    public List<ProjectIdAppEntity> getProjectIdAppEntitiesForUser(SafaUser user) {
        return getProjectsForUser(user).stream()
            .map(project -> projectService.getIdAppEntity(project, user))
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
            .map(ProjectMembership::getProject)
            .forEach(projects::add);

        teamMembershipService.getUserTeams(user)
            .stream()
            .flatMap(team -> projectService.getProjectsOwnedByTeam(team).stream())
            .forEach(projects::add);

        return projects;
    }

    /**
     * Returns list of members in given project for which the project was shared to them directly (rather than them
     * being on a team that has access).
     *
     * @param project The project whose members are retrieved.
     * @return List of project memberships relating members to projects.
     */
    public List<ProjectMembership> getProjectMembers(Project project) {
        return this.userProjectMembershipRepo.findByProject(project);
    }

    /**
     * Search for a project membership by its ID.
     *
     * @param membershipId The ID of the membership
     * @return The membership, if it exists
     */
    public Optional<ProjectMembership> getUserMembershipOptionalById(UUID membershipId) {
        return userProjectMembershipRepo.findById(membershipId);
    }

    /**
     * Search for a project membership by its ID. Throw an exception
     * if it's not found.
     *
     * @param membershipId The ID of the membership
     * @return The membership, if it exists
     * @throws SafaItemNotFoundError If the membership could not be found
     */
    public ProjectMembership getUserMembershipById(UUID membershipId) {
        return getUserMembershipOptionalById(membershipId)
            .orElseThrow(() -> new SafaItemNotFoundError("No membership found with the specified ID"));
    }
}
