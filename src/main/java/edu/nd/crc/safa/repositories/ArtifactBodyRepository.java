package edu.nd.crc.safa.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.entities.ArtifactBody;
import edu.nd.crc.safa.entities.ArtifactType;
import edu.nd.crc.safa.entities.ProjectVersion;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactBodyRepository extends CrudRepository<ArtifactBody, UUID> {

    List<ArtifactBody> findByProjectVersionAndArtifactType(ProjectVersion projectVersion,
                                                           ArtifactType artifactType);

    List<ArtifactBody> findByProjectVersion(ProjectVersion projectVersion);
}
