package edu.nd.crc.safa.features.memberships.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.memberships.entities.db.ProjectMembership;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserProjectMembershipRepository extends CrudRepository<ProjectMembership, UUID> {
    List<ProjectMembership> findByMember(SafaUser user);

    List<ProjectMembership> findByProject(Project project);

    List<ProjectMembership> findByProjectAndMember(Project project, SafaUser user);

    List<ProjectMembership> findByProjectAndRoleIn(Project project, List<ProjectRole> roles);

    Optional<ProjectMembership> findByMemberAndProjectAndRole(SafaUser member,
                                                              Project project,
                                                              ProjectRole role);

    List<ProjectMembership> findByProjectAndMembershipIdIn(Project project, List<UUID> entityIds);
}
