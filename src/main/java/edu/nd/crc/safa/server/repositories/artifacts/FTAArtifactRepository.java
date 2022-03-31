package edu.nd.crc.safa.server.repositories.artifacts;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.FTAArtifact;
import edu.nd.crc.safa.server.entities.db.Project;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface FTAArtifactRepository extends CrudRepository<FTAArtifact, UUID>, IProjectEntityRetriever<FTAArtifact> {

    Optional<FTAArtifact> findByArtifact(Artifact artifact);

    List<FTAArtifact> findByArtifactProject(Project project);

    default List<FTAArtifact> getByProject(Project project) {
        return this.findByArtifactProject(project);
    }
}
