package edu.nd.crc.safa.database.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.database.entities.ArtifactBody;
import edu.nd.crc.safa.database.entities.ArtifactType;
import edu.nd.crc.safa.database.entities.Project;
import edu.nd.crc.safa.database.entities.ProjectVersion;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactBodyRepository extends CrudRepository<ArtifactBody, UUID> {

    List<ArtifactBody> findByProjectAndProjectVersionAndArtifactType(Project project,
                                                                     ProjectVersion projectVersion,
                                                                     ArtifactType artifactType);

    List<ArtifactBody> findByProjectAndProjectVersion(Project project,
                                                      ProjectVersion projectVersion);
}
