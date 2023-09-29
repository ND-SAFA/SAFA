package edu.nd.crc.safa.features.memberships.services;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.memberships.entities.db.ProjectMembership;
import edu.nd.crc.safa.features.memberships.repositories.UserProjectMembershipRepository;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Responsible for CRUD operations related to project memberships
 */
@Service
@AllArgsConstructor
public class MemberService implements IAppEntityService<MembershipAppEntity> {

    private UserProjectMembershipRepository userProjectMembershipRepository;

    /**
     * Retrieve project membership with given id. Throws error if not found.
     *
     * @param projectMembershipId ID of membership being retrieved.
     * @return The project membership.
     */
    public ProjectMembership getMembershipById(UUID projectMembershipId) {
        Optional<ProjectMembership> projectMembershipQuery =
            this.userProjectMembershipRepository.findById(projectMembershipId);
        if (projectMembershipQuery.isEmpty()) {
            throw new SafaError("Could not find membership with id: %s.", projectMembershipId);
        }
        return projectMembershipQuery.get();
    }

    @Override
    public List<MembershipAppEntity> getAppEntities(ProjectVersion projectVersion, SafaUser user) {
        Project project = projectVersion.getProject();

        List<MembershipAppEntity> members = this.userProjectMembershipRepository.findByProject(project)
            .stream()
            .map(MembershipAppEntity::new)
            .collect(Collectors.toList());

        // TODO pull members the right way
        addOwnerMember(projectVersion, members);

        return members;
    }

    private void addOwnerMember(ProjectVersion projectVersion, List<MembershipAppEntity> members) {
        SafaUser owner = projectVersion.getProject().getOwningTeam().getOrganization().getOwner();

        members.add(new MembershipAppEntity(
                new ProjectMembership(projectVersion.getProject(), owner, ProjectRole.OWNER)));
    }

    @Override
    public List<MembershipAppEntity> getAppEntitiesByIds(ProjectVersion projectVersion, SafaUser user,
                                                            List<UUID> appEntityIds) {
        List<MembershipAppEntity> members = this.userProjectMembershipRepository
            .findByProjectAndMembershipIdIn(projectVersion.getProject(), appEntityIds)
            .stream()
            .map(MembershipAppEntity::new)
            .collect(Collectors.toList());
        addOwnerMember(projectVersion, members);
        return members;
    }

    /**
     * Returns list of members in given project with any of the given roles.
     *
     * @param project      The project whose members are retrieved.
     * @param projectRoles The project roles to match.
     * @return List of project memberships relating members to projects.
     */
    public List<ProjectMembership> getProjectMembersWithRoles(Project project, List<ProjectRole> projectRoles) {
        return this.userProjectMembershipRepository.findByProjectAndRoleIn(project, projectRoles);
    }

    /**
     * Returns list of members in given project with the given role.
     *
     * @param project     The project whose members are retrieved.
     * @param projectRole The project role to match.
     * @return List of project memberships relating members to projects.
     */
    public List<ProjectMembership> getProjectMembersWithRole(Project project, ProjectRole projectRole) {
        return getProjectMembersWithRoles(project, List.of(projectRole));
    }

    /**
     * Deletes project membership effectively removing user from
     * associated project
     *
     * @param projectMembershipId ID of the membership linking user and project.
     * @return ProjectMembers The membership object identified by given id, or null if none found.
     */
    public ProjectMembership deleteProjectMembershipById(UUID projectMembershipId) {
        Optional<ProjectMembership> projectMembershipQuery =
            this.userProjectMembershipRepository.findById(projectMembershipId);
        if (projectMembershipQuery.isPresent()) {
            ProjectMembership projectMembership = projectMembershipQuery.get();
            this.userProjectMembershipRepository.delete(projectMembership);
            return projectMembership;
        }
        return null;
    }
}
