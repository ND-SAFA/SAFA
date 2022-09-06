package edu.nd.crc.safa.features.projects.repositories;

import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProjectRepository extends CrudRepository<Project, UUID> {
    Project findByProjectId(UUID projectId);
}
