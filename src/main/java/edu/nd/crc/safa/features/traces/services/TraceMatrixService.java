package edu.nd.crc.safa.features.traces.services;

import java.util.Optional;

import edu.nd.crc.safa.features.traces.entities.db.TraceMatrixEntry;
import edu.nd.crc.safa.features.traces.repositories.TraceMatrixRepository;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class TraceMatrixService {
    private TraceMatrixRepository repo;

    public Optional<TraceMatrixEntry> getBySourceTypeAndTargetType(ArtifactType sourceType, ArtifactType targetType) {
        return repo.getBySourceTypeAndTargetType(sourceType, targetType);
    }
}
