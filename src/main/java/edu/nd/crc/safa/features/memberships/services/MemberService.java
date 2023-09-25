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
        SafaUser owner = projectVersion.getProject().getOwningTeam().getOrganization().getOwner();
        members.add(new MembershipAppEntity(
                new ProjectMembership(projectVersion.getProject(), owner, ProjectRole.OWNER)));

        return members;
    }

}
