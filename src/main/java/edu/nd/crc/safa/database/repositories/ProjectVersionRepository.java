package edu.nd.crc.safa.database.repositories;

import java.util.UUID;

import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.entities.ProjectVersion;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProjectVersionRepository extends CrudRepository<ProjectVersion, UUID> {

    ProjectVersion findTopByProjectOrderByVersionIdDesc(Project project);

    void deleteAllByProject(Project project);
}
