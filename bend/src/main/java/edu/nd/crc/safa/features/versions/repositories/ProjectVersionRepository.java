package edu.nd.crc.safa.features.versions.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProjectVersionRepository extends CrudRepository<ProjectVersion, UUID> {

    default Optional<ProjectVersion> getCurrentVersion(Project project) {
        return findTopByProjectOrderByMajorVersionDescMinorVersionDescRevisionDesc(project);
    }

    Optional<ProjectVersion> findTopByProjectOrderByMajorVersionDescMinorVersionDescRevisionDesc(Project project);

    List<ProjectVersion> findByProject(Project project);

    default List<ProjectVersion> findByProjectInBackwardsOrder(Project project) {
        return findByProjectOrderByMajorVersionDescMinorVersionDescRevisionDesc(project);
    }

    List<ProjectVersion> findByProjectOrderByMajorVersionDescMinorVersionDescRevisionDesc(Project project);

    ProjectVersion findByVersionId(UUID versionId);
}
