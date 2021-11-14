package edu.nd.crc.safa.server.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.TraceApproval;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.entities.db.TraceType;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TraceLinkRepository extends CrudRepository<TraceLink, UUID> {

    default List<TraceLink> getApprovedLinks(Project project) {
        return findBySourceArtifactProjectAndApprovalStatus(project, TraceApproval.APPROVED);
    }

    default List<TraceLink> getGeneratedLinks(Project project) {
        return findBySourceArtifactProjectAndTraceType(project, TraceType.GENERATED);
    }

    default List<TraceLink> getUnDeclinedLinks(Project project) {
        return findBySourceArtifactProjectAndApprovalStatusNot(project, TraceApproval.DECLINED);
    }

    default List<TraceLink> getLinks(Project project) {
        return findBySourceArtifactProject(project);
    }

    default Optional<TraceLink> getApprovedLinkIfExist(Artifact sourceArtifact, Artifact targetArtifact) {
        return findBySourceArtifactAndTargetArtifactAndApprovalStatus(sourceArtifact, targetArtifact, TraceApproval.APPROVED);
    }

    Optional<TraceLink> findBySourceArtifactAndTargetArtifactAndApprovalStatus(Artifact sourceArtifact,
                                                                               Artifact targetArtifact,
                                                                               TraceApproval approvalStatus);

    List<TraceLink> findBySourceArtifactProjectAndTraceType(Project project, TraceType traceType);

    List<TraceLink> findBySourceArtifactProjectAndApprovalStatusNot(Project project, TraceApproval approvalStatus);

    List<TraceLink> findBySourceArtifactProjectAndApprovalStatus(Project project, TraceApproval approvalStatus);

    List<TraceLink> findBySourceArtifactProject(Project project);

    default Optional<TraceLink> getByProjectAndSourceAndTarget(Project project, String sourceName, String targetName) {
        return findBySourceArtifactProjectAndSourceArtifactNameAndTargetArtifactName(project, sourceName, targetName);
    }

    Optional<TraceLink> findBySourceArtifactProjectAndSourceArtifactNameAndTargetArtifactName(Project project,
                                                                                              String sourceName,
                                                                                              String targetName);
}
