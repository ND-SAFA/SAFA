package edu.nd.crc.safa.server.db.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.db.entities.sql.ArtifactType;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.TraceMatrix;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TraceMatrixRepository extends CrudRepository<TraceMatrix, UUID> {

    List<TraceMatrix> findByProject(Project project);

    Optional<TraceMatrix> findBySourceTypeAndTargetType(ArtifactType sourceType, ArtifactType targetType);
}
