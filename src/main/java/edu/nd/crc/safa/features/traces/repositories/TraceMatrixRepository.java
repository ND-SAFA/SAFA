package edu.nd.crc.safa.features.traces.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.traces.entities.db.TraceMatrixEntry;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.data.repository.CrudRepository;

public interface TraceMatrixRepository extends CrudRepository<TraceMatrixEntry, UUID> {
    Optional<TraceMatrixEntry> getByProjectVersionAndSourceTypeAndTargetType(ProjectVersion projectVersion,
                                                                             ArtifactType sourceType,
                                                                             ArtifactType targetType);

    Optional<TraceMatrixEntry> getById(UUID id);

    List<TraceMatrixEntry> getByProjectVersion(ProjectVersion projectVersion);

    List<TraceMatrixEntry> getByProjectVersionAndIdIn(ProjectVersion projectVersion, List<UUID> ids);
}
