package edu.nd.crc.safa.server.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.ArtifactType;
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

    default Optional<TraceMatrix> queryForMatrixInProject(Project project,
                                                          ArtifactType sourceArtifactType,
                                                          ArtifactType targetArtifactType
    ) {
        return findByProjectAndSourceArtifactTypeAndTargetArtifactType(project, sourceArtifactType, targetArtifactType);
    }

    Optional<TraceMatrix> findByProjectAndSourceArtifactTypeNameAndTargetArtifactTypeName(Project project,
                                                                                          String sourceArtifactTypeName,
                                                                                          String targetArtifactTypeName);

    Optional<TraceMatrix> findByProjectAndSourceArtifactTypeAndTargetArtifactType(Project project,
                                                                                  ArtifactType sourceArtifactType,
                                                                                  ArtifactType targetArtifactType);
}
