package edu.nd.crc.safa.features.users.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.ProjectMembership;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProjectMembershipRepository extends CrudRepository<ProjectMembership, UUID> {
    List<ProjectMembership> findByMember(SafaUser user);

    List<ProjectMembership> findByProject(Project project);

    Optional<ProjectMembership> findByProjectAndMember(Project project, SafaUser user);
}
