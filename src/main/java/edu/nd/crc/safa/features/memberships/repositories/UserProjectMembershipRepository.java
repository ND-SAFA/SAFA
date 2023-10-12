package edu.nd.crc.safa.features.memberships.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.memberships.entities.db.UserProjectMembership;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserProjectMembershipRepository extends CrudRepository<UserProjectMembership, UUID> {
    List<UserProjectMembership> findByMember(SafaUser user);

    List<UserProjectMembership> findByProject(Project project);

    Optional<UserProjectMembership> findByProjectAndMember(Project project, SafaUser user);

    List<UserProjectMembership> findByProjectAndRoleIn(Project project, List<ProjectRole> roles);

    Optional<UserProjectMembership> findByMemberAndProject(SafaUser member, Project project);

    List<UserProjectMembership> findByProjectAndMembershipIdIn(Project project, List<UUID> entityIds);
}
