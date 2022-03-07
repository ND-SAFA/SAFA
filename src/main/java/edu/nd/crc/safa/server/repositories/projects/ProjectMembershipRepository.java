package edu.nd.crc.safa.server.repositories.projects;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectMembership;
import edu.nd.crc.safa.server.entities.db.SafaUser;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProjectMembershipRepository extends CrudRepository<ProjectMembership, UUID> {
    List<ProjectMembership> findByMember(SafaUser user);

    List<ProjectMembership> findByProject(Project project);

    Optional<ProjectMembership> findByProjectAndMember(Project project, SafaUser user);
}
