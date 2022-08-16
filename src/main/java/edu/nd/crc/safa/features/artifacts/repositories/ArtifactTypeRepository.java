package edu.nd.crc.safa.features.artifacts.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.types.ArtifactType;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactTypeRepository extends CrudRepository<ArtifactType, UUID> {

    Optional<ArtifactType> findByProjectAndNameIgnoreCase(Project project, String name);

    ArtifactType findByTypeId(UUID typeId);

    List<ArtifactType> findByProject(Project project);
}
