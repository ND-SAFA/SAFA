package edu.nd.crc.safa.db.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.TraceLink;
import edu.nd.crc.safa.db.entities.sql.TraceType;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TraceLinkRepository extends CrudRepository<TraceLink, UUID> {

    List<TraceLink> findBySourceArtifactProject(Project project);

    default List<TraceLink> findByProject(Project project) {
        return findBySourceArtifactProject(project);
    }

    default void deleteAllByProjectAndTraceType(Project project, TraceType traceType) {
        deleteAllBySourceArtifactProjectAndTraceType(project, traceType);
    }

    void deleteAllBySourceArtifactProjectAndTraceType(Project project, TraceType traceType);
}
