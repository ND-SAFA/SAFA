package edu.nd.crc.safa.database.repositories;

import java.util.UUID;

import edu.nd.crc.safa.entities.ArtifactType;
import edu.nd.crc.safa.entities.Project;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactTypeRepository extends CrudRepository<ArtifactType, UUID> {

    ArtifactType findByProjectAndName(Project project, String name);

    ArtifactType findByTypeId(UUID typeId);
}
