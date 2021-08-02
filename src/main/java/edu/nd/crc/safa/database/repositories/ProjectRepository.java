package edu.nd.crc.safa.database.repositories;

import java.util.UUID;

import edu.nd.crc.safa.database.entities.Project;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProjectRepository extends CrudRepository<Project, UUID> {
    Project findByProjectId(UUID projectId);
}
