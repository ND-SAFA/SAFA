package edu.nd.crc.safa.repositories;

import java.util.UUID;

import edu.nd.crc.safa.entities.database.Project;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProjectRepository extends CrudRepository<Project, UUID> {
    Project findByProjectId(UUID projectId); // TODO: remove and use findById and deal with optional.
}
