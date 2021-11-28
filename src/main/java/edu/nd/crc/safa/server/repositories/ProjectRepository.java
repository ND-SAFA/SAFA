package edu.nd.crc.safa.server.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.SafaUser;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProjectRepository extends CrudRepository<Project, UUID> {
    Project findByProjectId(UUID projectId); // TODO: remove and use findById and deal with optional.

    List<Project> findByOwner(SafaUser owner);
}
