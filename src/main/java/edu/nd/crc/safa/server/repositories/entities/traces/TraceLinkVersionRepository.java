package edu.nd.crc.safa.server.repositories.entities.traces;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceApproval;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.server.repositories.entities.artifacts.IVersionRepository;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TraceLinkVersionRepository extends CrudRepository<TraceLinkVersion, UUID>,
    IVersionRepository<TraceLinkVersion, TraceAppEntity> {

    default List<TraceLinkVersion> getApprovedLinksInVersion(ProjectVersion projectVersion) {
        return findByProjectVersionAndApprovalStatus(projectVersion, TraceApproval.APPROVED);
    }

    default List<TraceLinkVersion> getApprovedLinksInProject(Project project) {
        return findByProjectVersionProjectAndApprovalStatus(project, TraceApproval.APPROVED);
    }

    default List<TraceLinkVersion> getProjectLinks(Project project) {
        return findByProjectVersionProject(project);
    }

    default Optional<TraceLinkVersion> getApprovedLinkIfExist(Artifact sourceArtifact, Artifact targetArtifact) {
        return findByTraceLinkSourceArtifactAndTraceLinkTargetArtifactAndApprovalStatus(sourceArtifact, targetArtifact,
            TraceApproval.APPROVED);
    }

    List<TraceLinkVersion> findByProjectVersionProject(Project project);

    List<TraceLinkVersion> findByTraceLink(TraceLink traceLink);

    List<TraceLinkVersion> findByTraceLinkTraceLinkId(UUID traceLinkId);

    Optional<TraceLinkVersion> findByTraceLinkSourceArtifactAndTraceLinkTargetArtifactAndApprovalStatus(
        Artifact sourceArtifact,
        Artifact targetArtifact,
        TraceApproval approvalStatus);

    List<TraceLinkVersion> findByProjectVersionProjectAndApprovalStatus(Project project,
                                                                        TraceApproval approvalStatus);

    List<TraceLinkVersion> findByProjectVersionAndApprovalStatus(ProjectVersion projectVersion,
                                                                 TraceApproval approvalStatus);

    Optional<TraceLinkVersion> findByProjectVersionAndTraceLink(ProjectVersion projectVersion, TraceLink traceLink);

    default Optional<TraceLinkVersion> findByProjectVersionAndSourceAndTarget(ProjectVersion projectVersion,
                                                                              String source,
                                                                              String target) {
        return findByProjectVersionAndTraceLinkSourceArtifactNameAndTraceLinkTargetArtifactName(projectVersion, source,
            target);
    }

    Optional<TraceLinkVersion> findByProjectVersionAndTraceLinkSourceArtifactNameAndTraceLinkTargetArtifactName(ProjectVersion projectVersion, String source, String target);

}
