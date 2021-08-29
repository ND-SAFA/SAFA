package edu.nd.crc.safa.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.entities.database.Artifact;
import edu.nd.crc.safa.entities.database.Project;
import edu.nd.crc.safa.entities.database.TraceLink;
import edu.nd.crc.safa.entities.database.TraceType;

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
