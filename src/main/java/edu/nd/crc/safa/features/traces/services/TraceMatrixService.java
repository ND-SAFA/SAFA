package edu.nd.crc.safa.features.traces.services;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.projects.entities.app.TraceMatrixAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.TraceMatrixEntry;
import edu.nd.crc.safa.features.traces.repositories.TraceMatrixRepository;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class TraceMatrixService implements IAppEntityService<TraceMatrixAppEntity> {
    private TraceMatrixRepository repo;

    public Optional<TraceMatrixEntry> getEntry(ProjectVersion projectVersion, ArtifactType sourceType,
                                               ArtifactType targetType) {
        return repo.getByProjectVersionAndSourceTypeAndTargetType(projectVersion, sourceType, targetType);
    }

    public void save(TraceMatrixEntry traceMatrixEntry) {
        repo.save(traceMatrixEntry);
    }

    @Override
    public List<TraceMatrixAppEntity> getAppEntities(ProjectVersion projectVersion, SafaUser user) {
        return repo.getByProjectVersion(projectVersion).stream()
            .map(TraceMatrixAppEntity::new)
            .collect(Collectors.toList());
    }
}
