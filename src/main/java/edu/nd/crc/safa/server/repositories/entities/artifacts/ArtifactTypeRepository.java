package edu.nd.crc.safa.server.repositories.entities.artifacts;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.Project;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactTypeRepository extends CrudRepository<ArtifactType, UUID> {

    Optional<ArtifactType> findByProjectAndNameIgnoreCase(Project project, String name);

    ArtifactType findByTypeId(UUID typeId);

    List<ArtifactType> findByProject(Project project);
}
