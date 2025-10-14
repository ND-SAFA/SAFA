package edu.nd.crc.safa.features.types.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.types.entities.db.ArtifactTypeCount;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.data.repository.CrudRepository;

public interface ArtifactTypeCountRepository extends CrudRepository<ArtifactTypeCount, UUID> {
    List<ArtifactTypeCount> getByProjectVersion(ProjectVersion projectVersion);

    List<ArtifactTypeCount> getByType(ArtifactType type);

    Optional<ArtifactTypeCount> getByProjectVersionAndType(ProjectVersion projectVersion, ArtifactType type);
}
