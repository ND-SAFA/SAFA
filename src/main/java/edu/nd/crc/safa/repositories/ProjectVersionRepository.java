package edu.nd.crc.safa.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.entities.database.Project;
import edu.nd.crc.safa.entities.database.ProjectVersion;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProjectVersionRepository extends CrudRepository<ProjectVersion, UUID> {

    ProjectVersion findTopByProjectOrderByVersionIdDesc(Project project);

    List<ProjectVersion> findByProject(Project project);
}
