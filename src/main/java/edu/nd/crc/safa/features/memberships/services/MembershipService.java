package edu.nd.crc.safa.features.memberships.services;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.memberships.repositories.UserProjectMembershipRepository;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
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
public class MembershipService implements IAppEntityService<MembershipAppEntity> {
    private TeamMembershipService teamMembershipService;
    private UserProjectMembershipRepository userProjectMembershipRepository;

    @Override
    public List<MembershipAppEntity> getAppEntities(ProjectVersion projectVersion, SafaUser requester) {
        Project project = projectVersion.getProject();
        List<MembershipAppEntity> projectMembers = teamMembershipService.getProjectMemberships(project);
        List<MembershipAppEntity> invitedMembers = this.userProjectMembershipRepository.findByProject(project)
            .stream()
            .map(MembershipAppEntity::new)
            .collect(Collectors.toList());
        projectMembers.addAll(invitedMembers);
        return projectMembers;
    }

    @Override
    public List<MembershipAppEntity> getAppEntitiesByIds(ProjectVersion projectVersion, SafaUser user,
                                                         List<UUID> appEntityIds) {
        return this.userProjectMembershipRepository
            .findByProjectAndMembershipIdIn(projectVersion.getProject(), appEntityIds)
            .stream()
            .map(MembershipAppEntity::new)
            .collect(Collectors.toList());
    }
}
