package edu.nd.crc.safa.server.db.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.db.entities.sql.Artifact;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.TraceLink;
import edu.nd.crc.safa.server.db.entities.sql.TraceType;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TraceLinkRepository extends CrudRepository<TraceLink, UUID> {

    default List<TraceLink> getApprovedLinks(Project project) {
        return findBySourceArtifactProjectAndApproved(project, true);
    }

    default List<TraceLink> getGeneratedLinks(Project project) {
        return findBySourceArtifactProjectAndTraceType(project, TraceType.GENERATED);
    }

    default List<TraceLink> getManualLinks(Project project) {
        return findBySourceArtifactProjectAndTraceType(project, TraceType.MANUAL);
    }

    default Optional<TraceLink> getApprovedLinkIfExist(Artifact sourceArtifact, Artifact targetArtifact) {
        return findBySourceArtifactAndTargetArtifactAndApproved(sourceArtifact, targetArtifact, true);
    }

    Optional<TraceLink> findBySourceArtifactAndTargetArtifactAndApproved(Artifact sourceArtifact,
                                                                         Artifact targetArtifact,
                                                                         boolean approved);

    List<TraceLink> findBySourceArtifactProjectAndTraceType(Project project, TraceType traceType);

    List<TraceLink> findBySourceArtifactProjectAndApproved(Project project, boolean approved);
}
