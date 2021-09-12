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

    List<TraceLink> findBySourceArtifactProject(Project project);

    default List<TraceLink> findByProject(Project project) {
        return findBySourceArtifactProject(project);
    }

    Optional<TraceLink> findBySourceArtifactAndTargetArtifact(Artifact sourceArtifact, Artifact targetArtifact);
}
