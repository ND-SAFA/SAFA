package edu.nd.crc.safa.server.db.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.db.entities.sql.Artifact;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.TraceLink;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TraceLinkRepository extends CrudRepository<TraceLink, UUID> {
    
    default List<TraceLink> getApprovedLinks(Project project) {
        return findBySourceArtifactProjectAndApproved(project, true);
    }

    default Optional<TraceLink> getApprovedLinkIfExist(Artifact sourceArtifact, Artifact targetArtifact) {
        return findBySourceArtifactAndTargetArtifactAndApproved(sourceArtifact, targetArtifact, true);
    }

    Optional<TraceLink> findBySourceArtifactAndTargetArtifactAndApproved(Artifact sourceArtifact,
                                                                         Artifact targetArtifact,
                                                                         boolean approved);

    default List<TraceLink> getProjectGeneratedLinks(Project project) {
        return findBySourceArtifactProjectAndApproved(project, false);
    }

    default List<TraceLink> getProjectApprovedLinks(Project project) {
        return findBySourceArtifactProjectAndApproved(project, true);
    }

    List<TraceLink> findBySourceArtifactProjectAndApproved(Project project, boolean approved);
}
