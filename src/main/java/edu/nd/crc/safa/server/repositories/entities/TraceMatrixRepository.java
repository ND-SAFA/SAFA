package edu.nd.crc.safa.server.repositories.entities;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.TraceMatrix;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TraceMatrixRepository extends CrudRepository<TraceMatrix, UUID> {
    List<TraceMatrix> findByProject(Project project);

    default Optional<TraceMatrix> queryForMatrixInProject(Project project,
                                                          String sourceArtifactTypeName,
                                                          String targetArtifactTypeName) {
        return findByProjectAndSourceArtifactTypeNameAndTargetArtifactTypeName(project,
            sourceArtifactTypeName,
            targetArtifactTypeName);
    }

    Optional<TraceMatrix> findByProjectAndSourceArtifactTypeNameAndTargetArtifactTypeName(
        Project project,
        String sourceArtifactTypeName,
        String targetArtifactTypeName);
}
