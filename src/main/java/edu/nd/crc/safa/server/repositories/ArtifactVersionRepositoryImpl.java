package edu.nd.crc.safa.server.repositories;

import java.util.List;

import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.Project;

import org.springframework.beans.factory.annotation.Autowired;

/**
 * Implements custom any custom artifact repository logic.
 */
public class ArtifactVersionRepositoryImpl extends GenericVersionRepository<ArtifactVersion> {

    @Autowired
    ArtifactVersionRepository artifactVersionRepository;

    @Override
    public List<ArtifactVersion> getEntitiesInProject(Project project) {
        return artifactVersionRepository.findByProjectVersionProject(project);
    }
}
