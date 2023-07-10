package edu.nd.crc.safa.features.traces.repositories;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.traces.entities.db.TraceMatrixEntry;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;

import org.springframework.data.repository.CrudRepository;

public interface TraceMatrixRepository extends CrudRepository<TraceMatrixEntry, UUID> {
    Optional<TraceMatrixEntry> getBySourceTypeAndTargetType(ArtifactType sourceType, ArtifactType targetType);
}
