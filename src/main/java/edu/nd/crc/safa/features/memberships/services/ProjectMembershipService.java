package edu.nd.crc.safa.features.memberships.services;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.memberships.entities.db.IEntityMembership;
import edu.nd.crc.safa.features.memberships.entities.db.ProjectMembership;
import edu.nd.crc.safa.features.memberships.repositories.UserProjectMembershipRepository;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipType;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.IRole;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.permissions.entities.TeamPermission;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.projects.entities.app.ProjectIdAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class ProjectMembershipService implements IMembershipService {

    private final ProjectService projectService;
    private final UserProjectMembershipRepository userProjectMembershipRepo;
    private final TeamMembershipService teamMembershipService;
    private final NotificationService notificationService;
    private final PermissionService permissionService;

    /**
     * {@inheritDoc}
     */
    @Override
    public ProjectMembership addUserRole(SafaUser user, IEntityWithMembership entity, IRole iRole) {
        assert entity instanceof Project;
        assert iRole instanceof ProjectRole;
        Project project = (Project) entity;
        ProjectRole role = (ProjectRole) iRole;

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
     * {@inheritDoc}
     */
    @Override
    public void removeUserRole(SafaUser user, IEntityWithMembership entity, IRole iRole) {
        assert entity instanceof Project;
        assert iRole instanceof ProjectRole;
        Project project = (Project) entity;
        ProjectRole role = (ProjectRole) iRole;

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
     * {@inheritDoc}
     */
    @Override
    public List<IRole> getRolesForUser(SafaUser user, IEntityWithMembership entity) {
        assert entity instanceof Project;
        Project project = (Project) entity;
        return userProjectMembershipRepo.findByProjectAndMember(project, user).stream()
            .map(ProjectMembership::getRole)
            .collect(Collectors.toUnmodifiableList());
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public List<IEntityMembership> getMembershipsForUser(SafaUser user) {
        // Remaking the list forces it to understand that the type is indeed correct
        return new ArrayList<>(userProjectMembershipRepo.findByMember(user));
    }

    /**
     * Returns list of projects owned or shared with current user.
     *
     * @param user The user to get projects for
     * @return List of projects where given user has access to.
     */
    public List<ProjectIdAppEntity> getProjectIdAppEntitiesForUser(SafaUser user) {
        return getProjectsForUser(user).stream()
            .filter(project -> permissionService.hasAnyPermission(
                Set.of(TeamPermission.VIEW_PROJECTS, ProjectPermission.VIEW), project, user
            )).map(project -> projectService.getIdAppEntity(project, user))
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

        teamMembershipService.getEntitiesForUser(user)
            .stream()
            .flatMap(team -> projectService.getProjectsOwnedByTeam((Team) team).stream())
            .forEach(projects::add);

        return projects;
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public List<IEntityMembership> getMembershipsForEntity(IEntityWithMembership entity) {
        assert entity instanceof Project;
        Project project = (Project) entity;
        // Remaking the list forces it to understand that the type is indeed correct
        return new ArrayList<>(this.userProjectMembershipRepo.findByProject(project));
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public Optional<IEntityMembership> getMembershipOptionalById(UUID membershipId) {
        // The map call forces it to understand that the type is indeed correct
        return userProjectMembershipRepo.findById(membershipId).map(m -> m);
    }

    /**
     * Returns the individually invited members of the project.
     *
     * @param project Project whose members are returned.
     * @return List of members with whom the project is directly shared
     */
    public List<MembershipAppEntity> getProjectMemberships(Project project) {
        List<IEntityMembership> projectMembers = this.getMembershipsForEntity(project);
        return projectMembers
            .stream()
            .map(m -> {
                MembershipAppEntity membershipAppEntity = new MembershipAppEntity();
                membershipAppEntity.setEntityType(MembershipType.PROJECT);
                membershipAppEntity.setEntityId(project.getId());
                membershipAppEntity.setEmail(m.getUser().getEmail());
                membershipAppEntity.setRole(m.getRole().name());
                return membershipAppEntity;
            }).collect(Collectors.toList());
    }
}
