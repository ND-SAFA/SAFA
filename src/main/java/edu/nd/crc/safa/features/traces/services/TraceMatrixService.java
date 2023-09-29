package edu.nd.crc.safa.features.traces.services;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.traces.entities.app.TraceMatrixAppEntity;
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

    /**
     * Get the trace matrix entry associated with a project version and source and target artifact types
     *
     * @param projectVersion The project version
     * @param sourceType     The source type
     * @param targetType     The target type
     * @return The entry, if it exists
     */
    public Optional<TraceMatrixEntry> getEntry(ProjectVersion projectVersion, ArtifactType sourceType,
                                               ArtifactType targetType) {
        return repo.getByProjectVersionAndSourceTypeAndTargetType(projectVersion, sourceType, targetType);
    }

    /**
     * Get the trace matrix entry with the given ID
     *
     * @param traceMatrixId The ID of the entry
     * @return The entry, if it exists
     */
    public Optional<TraceMatrixEntry> getEntry(UUID traceMatrixId) {
        return repo.getById(traceMatrixId);
    }

    /**
     * Create a new trace matrix entry for the given version and types
     *
     * @param projectVersion The project version
     * @param sourceType     The source type
     * @param targetType     The target type
     * @return The newly created trace entry
     */
    public TraceMatrixEntry createEntry(ProjectVersion projectVersion, ArtifactType sourceType,
                                        ArtifactType targetType) {
        Optional<TraceMatrixEntry> entry = getEntry(projectVersion, sourceType, targetType);
        if (entry.isPresent()) {
            throw new SafaError("Entry already exists for the given types");
        }

        TraceMatrixEntry newEntry = new TraceMatrixEntry(projectVersion, sourceType, targetType);
        return repo.save(newEntry);
    }

    /**
     * Retrieves the entry associated with the parameters, creating it if needed
     *
     * @param projectVersion The project version
     * @param sourceType     The source type
     * @param targetType     The target type
     * @return The entry
     */
    public TraceMatrixEntry getOrCreateEntry(ProjectVersion projectVersion, ArtifactType sourceType,
                                             ArtifactType targetType) {
        Optional<TraceMatrixEntry> entry = getEntry(projectVersion, sourceType, targetType);
        return entry.orElseGet(() -> createEntry(projectVersion, sourceType, targetType));
    }

    /**
     * Update an entry in the database
     *
     * @param traceMatrixEntry The entry to save
     */
    public void updateEntry(TraceMatrixEntry traceMatrixEntry) {
        if (traceMatrixEntry.getId() == null) {
            throw new SafaError("Use createEntry() to create a new trace matrix entry");
        }
        repo.save(traceMatrixEntry);
    }

    /**
     * Delete an entry from the database
     *
     * @param traceMatrixEntry The entry to delete
     */
    public void delete(TraceMatrixEntry traceMatrixEntry) {
        repo.delete(traceMatrixEntry);
    }

    @Override
    public List<TraceMatrixAppEntity> getAppEntities(ProjectVersion projectVersion, SafaUser user) {
        return getEntries(projectVersion).stream()
            .map(TraceMatrixAppEntity::new)
            .collect(Collectors.toList());
    }

    @Override
    public List<TraceMatrixAppEntity> getAppEntitiesByIds(ProjectVersion projectVersion, SafaUser user,
                                                          List<UUID> appEntityIds) {
        return repo.getByProjectVersionAndIdIn(projectVersion, appEntityIds)
            .stream()
            .map(TraceMatrixAppEntity::new)
            .collect(Collectors.toList());
    }

    /**
     * Get all entries associated with a project version
     *
     * @param projectVersion The project version
     * @return The trace matrix entries in that version
     */
    public List<TraceMatrixEntry> getEntries(ProjectVersion projectVersion) {
        return repo.getByProjectVersion(projectVersion);
    }
}
