package edu.nd.crc.safa.server.repositories;

import java.util.List;

import edu.nd.crc.safa.server.entities.db.ArtifactBody;
import edu.nd.crc.safa.server.entities.db.Project;

import org.springframework.beans.factory.annotation.Autowired;

/**
 * Implements custom any custom artifact repository logic.
 */
public class ArtifactBodyRepositoryImpl extends GenericVersionRepository<ArtifactBody> {

    @Autowired
    ArtifactBodyRepository artifactBodyRepository;

    @Override
    public List<ArtifactBody> getEntitiesInProject(Project project) {
        return artifactBodyRepository.findByProjectVersionProject(project);
    }
}
