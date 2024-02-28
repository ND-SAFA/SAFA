package edu.nd.crc.safa.features.traces.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.repositories.IVersionRepository;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceLink;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TraceLinkVersionRepository extends CrudRepository<TraceLinkVersion, UUID>,
    IVersionRepository<TraceLinkVersion, TraceAppEntity> {

    default List<TraceLinkVersion> getTraceVersionsRelatedToArtifacts(List<UUID> artifactIds) {
        return findByTraceLinkSourceArtifactArtifactIdInOrTraceLinkTargetArtifactArtifactIdIn(artifactIds, artifactIds);
    }

    List<TraceLinkVersion> findByTraceLinkSourceArtifactArtifactIdInOrTraceLinkTargetArtifactArtifactIdIn(
        List<UUID> artifactIdsOne, List<UUID> artifactIdsTwo);

    default List<TraceLinkVersion> getApprovedLinksInVersion(ProjectVersion projectVersion) {
        return findByProjectVersionAndApprovalStatus(projectVersion, ApprovalStatus.APPROVED);
    }

    default List<TraceLinkVersion> getApprovedLinksInProject(Project project) {
        return findByProjectVersionProjectAndApprovalStatus(project, ApprovalStatus.APPROVED);
    }

    default List<TraceLinkVersion> getProjectLinks(Project project) {
        return findByProjectVersionProject(project);
    }

    List<TraceLinkVersion> findByProjectVersionProject(Project project);

    List<TraceLinkVersion> findByTraceLink(TraceLink traceLink);

    List<TraceLinkVersion> findByTraceLinkTraceLinkIdIn(List<UUID> traceLinkIds);

    List<TraceLinkVersion> findByTraceLinkTraceLinkId(UUID traceLinkId);

    List<TraceLinkVersion> findByProjectVersionProjectAndApprovalStatus(Project project,
                                                                        ApprovalStatus approvalStatus);

    List<TraceLinkVersion> findByProjectVersionAndApprovalStatus(ProjectVersion projectVersion,
                                                                 ApprovalStatus approvalStatus);

    Optional<TraceLinkVersion> findByProjectVersionAndTraceLink(ProjectVersion projectVersion, TraceLink traceLink);

    int countByProjectVersion(ProjectVersion projectVersion);
}
