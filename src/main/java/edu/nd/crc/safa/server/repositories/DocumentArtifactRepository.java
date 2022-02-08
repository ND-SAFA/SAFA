package edu.nd.crc.safa.server.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.DocumentArtifact;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DocumentArtifactRepository extends CrudRepository<DocumentArtifact, UUID> {

    List<DocumentArtifact> findByProjectVersionAndArtifact(ProjectVersion projectVersion, Artifact artifact);
}
