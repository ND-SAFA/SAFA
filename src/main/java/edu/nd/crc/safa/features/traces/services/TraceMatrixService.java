package edu.nd.crc.safa.features.traces.services;

import java.util.Optional;

import edu.nd.crc.safa.features.traces.entities.db.TraceMatrixEntry;
import edu.nd.crc.safa.features.traces.repositories.TraceMatrixRepository;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class TraceMatrixService {
    private TraceMatrixRepository repo;

    public Optional<TraceMatrixEntry> getEntry(ProjectVersion projectVersion, ArtifactType sourceType,
                                               ArtifactType targetType) {
        return repo.getByProjectVersionAndSourceTypeAndTargetType(projectVersion, sourceType, targetType);
    }

    public void save(TraceMatrixEntry traceMatrixEntry) {
        repo.save(traceMatrixEntry);
    }
}
