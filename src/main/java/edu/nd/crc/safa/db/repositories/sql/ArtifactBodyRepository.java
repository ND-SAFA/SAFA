package edu.nd.crc.safa.db.repositories.sql;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.db.entities.sql.ArtifactType;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactBodyRepository extends CrudRepository<ArtifactBody, UUID> {

    List<ArtifactBody> findByProjectVersionAndArtifactType(ProjectVersion projectVersion,
                                                           ArtifactType artifactType);

    List<ArtifactBody> findByProjectVersion(ProjectVersion projectVersion);

    List<ArtifactBody> findByArtifactName(String name);
}
