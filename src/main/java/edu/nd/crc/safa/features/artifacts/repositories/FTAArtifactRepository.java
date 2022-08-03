package edu.nd.crc.safa.features.artifacts.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.FTAArtifact;
import edu.nd.crc.safa.features.projects.entities.app.IProjectEntityRetriever;
import edu.nd.crc.safa.features.projects.entities.db.Project;

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
