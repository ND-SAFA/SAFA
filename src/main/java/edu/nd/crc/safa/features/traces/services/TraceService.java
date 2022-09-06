package edu.nd.crc.safa.features.traces.services;

import java.util.List;
import java.util.UUID;
import java.util.function.Predicate;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class TraceService implements IAppEntityService<TraceAppEntity> {
    ArtifactService artifactService;
    TraceLinkVersionRepository traceLinkVersionRepository;

    @Override
    public List<TraceAppEntity> getAppEntities(ProjectVersion projectVersion) {
        return getAppEntities(projectVersion, t -> t.getApprovalStatus() != ApprovalStatus.DECLINED);
    }

    public List<TraceAppEntity> getAppEntities(ProjectVersion projectVersion,
                                               Predicate<TraceAppEntity> tracePredicate) {
        List<ArtifactAppEntity> projectVersionArtifacts = artifactService
            .getAppEntities(projectVersion);
        List<UUID> projectVersionArtifactIds = projectVersionArtifacts
            .stream()
            .map(ArtifactAppEntity::getId)
            .collect(Collectors.toList());
        return retrieveActiveTracesInProjectVersion(projectVersion, projectVersionArtifactIds, tracePredicate);
    }

    /**
     * Returns trace links associated with given artifacts at the specified version.
     *
     * @param projectVersion      The version of the artifacts and associated traces to retrieve.
     * @param existingArtifactIds Artifact IDs of trace links to retrieve.
     * @return List of {@link TraceAppEntity} Traces associated with existing artifact IDs.
     */
    public List<TraceAppEntity> retrieveActiveTracesInProjectVersion(ProjectVersion projectVersion,
                                                                     List<UUID> existingArtifactIds) {
        return retrieveActiveTracesInProjectVersion(projectVersion, existingArtifactIds,
            t -> t.getApprovalStatus() != ApprovalStatus.DECLINED);
    }

    public List<TraceAppEntity> retrieveActiveTracesInProjectVersion(ProjectVersion projectVersion,
                                                                     List<UUID> existingArtifactIds,
                                                                     Predicate<TraceAppEntity> tracePredicate) {
        return this.traceLinkVersionRepository
            .retrieveAppEntitiesByProjectVersion(projectVersion)
            .stream()
            .filter(t -> existingArtifactIds.contains(t.getSourceId())
                && existingArtifactIds.contains(t.getTargetId()))
            .filter(tracePredicate)
            .collect(Collectors.toList());
        //TODO: Look at absorbing filter method into the retrieval method by default.
    }

    /**
     * Returns list of traces current active in project version containing
     * source or target as given artifact.
     *
     * @param projectVersion The project version used to retrieve active links.
     * @param artifactName   The artifact to be used to query links.
     * @return List of traces active in version and associated with artifact
     */
    public List<TraceAppEntity> getTracesInProjectVersionRelatedToArtifact(
        ProjectVersion projectVersion,
        String artifactName
    ) {
        return this.traceLinkVersionRepository
            .retrieveAppEntitiesByProjectVersion(projectVersion)
            .stream()
            .filter(t -> artifactName.equals(t.getSourceName()) || artifactName.equals(t.getTargetName()))
            .collect(Collectors.toList());
    }
}
