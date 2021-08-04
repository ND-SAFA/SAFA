package edu.nd.crc.safa.database.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.entities.TraceLink;
import edu.nd.crc.safa.entities.TraceType;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TraceLinkRepository extends CrudRepository<TraceLink, UUID> {

    List<TraceLink> findByProject(Project project);

    void deleteAllByProjectAndTraceType(Project project, TraceType traceType);
}
