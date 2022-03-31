package edu.nd.crc.safa.server.repositories.artifacts;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.SafetyCaseArtifact;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface SafetyCaseArtifactRepository extends
    CrudRepository<SafetyCaseArtifact, UUID>, IProjectEntityRetriever<SafetyCaseArtifact> {

    List<SafetyCaseArtifact> findByArtifactProject(Project project);

    Optional<SafetyCaseArtifact> findByArtifact(Artifact artifact);

    default List<SafetyCaseArtifact> getByProject(Project project) {
        return this.findByArtifactProject(project);
    }
}
