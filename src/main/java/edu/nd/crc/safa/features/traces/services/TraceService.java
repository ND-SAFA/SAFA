package edu.nd.crc.safa.features.traces.services;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.function.Predicate;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkVersionRepositoryImpl;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.VersionCalculator;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class TraceService implements IAppEntityService<TraceAppEntity> {
    ArtifactService artifactService;
    TraceLinkVersionRepository traceLinkVersionRepository;
    TraceLinkVersionRepositoryImpl traceLinkVersionRepositoryImpl;

    @Override
    public List<TraceAppEntity> getAppEntities(ProjectVersion projectVersion, SafaUser user) {
        return getAppEntities(projectVersion, user, TraceAppEntity::isVisible);
    }

    /**
     * Retrieves list of filtered trace links at given version.
     *
     * @param projectVersion The version of the trace links to retrieve.
     * @param user           The user making the request
     * @param tracePredicate The filtering predicate, returns link if true on predicate.
     * @return List of filtered trace links.
     */
    public List<TraceAppEntity> getAppEntities(ProjectVersion projectVersion, SafaUser user,
                                               Predicate<TraceAppEntity> tracePredicate) {
        List<ArtifactAppEntity> projectVersionArtifacts = artifactService
            .getAppEntities(projectVersion, user);
        List<UUID> projectVersionArtifactIds = projectVersionArtifacts
            .stream()
            .map(ArtifactAppEntity::getId)
            .collect(Collectors.toList());
        return getTracesRelatedToArtifacts(projectVersion, projectVersionArtifactIds)
            .stream().filter(tracePredicate).collect(Collectors.toList());
    }

    /**
     * Returns trace links associated with given artifacts at the specified version.
     *
     * @param projectVersion      The version of the artifacts and associated traces to retrieve.
     * @param existingArtifactIds Artifact IDs of trace links to retrieve.
     * @return List of {@link TraceAppEntity} Traces associated with existing artifact IDs.
     */
    public List<TraceAppEntity> retrieveActiveTraces(ProjectVersion projectVersion,
                                                     List<UUID> existingArtifactIds) {
        return this.getTracesRelatedToArtifacts(projectVersion, existingArtifactIds)
            .stream()
            .filter(TraceAppEntity::isVisible)
            .collect(Collectors.toList());
    }

    /**
     * Returns list of traces current active in project version containing
     * source or target as given artifact.
     *
     * @param projectVersion The project version used to retrieve active links.
     * @param artifactIds    The artifact ids referenced by trace links.
     * @return List of traces active in version and associated with artifact
     */
    public List<TraceAppEntity> getTracesRelatedToArtifacts(
        ProjectVersion projectVersion,
        List<UUID> artifactIds
    ) {
        List<TraceLinkVersion> traceVersions = this.traceLinkVersionRepository.getTraceVersionsRelatedToArtifacts(
            artifactIds);
        Map<UUID, List<TraceLinkVersion>> baseEntityTable = ProjectDataStructures.groupEntitiesByProperty(
            traceVersions,
            TraceLinkVersion::getBaseEntityId
        );
        List<TraceLinkVersion> traceLinksAtVersion =
            VersionCalculator.calculateVersionEntitiesAtProjectVersion(projectVersion,
                baseEntityTable);
        return traceLinksAtVersion
            .stream()
            .filter(t -> t.getModificationType() != ModificationType.REMOVED)
            .map(this.traceLinkVersionRepository::retrieveAppEntityFromVersionEntity)
            .collect(Collectors.toList());
    }
}
