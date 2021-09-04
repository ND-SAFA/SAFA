package edu.nd.crc.safa.db.repositories.sql;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.db.entities.sql.Artifact;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.TraceLink;
import edu.nd.crc.safa.db.entities.sql.TraceType;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TraceLinkRepository extends CrudRepository<TraceLink, UUID> {

    List<TraceLink> findByProject(Project project);

    List<TraceLink> findByProjectAndTraceType(Project project, TraceType traceType);

    void deleteAllByProjectAndTraceType(Project project, TraceType traceType);

    Optional<TraceLink> findByProjectAndSourceArtifactAndTargetArtifact(Project project,
                                                                        Artifact sourceArtifact,
                                                                        Artifact targetArtifact);
}
