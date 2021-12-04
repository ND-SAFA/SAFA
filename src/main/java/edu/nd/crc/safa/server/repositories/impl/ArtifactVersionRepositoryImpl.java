package edu.nd.crc.safa.server.repositories.impl;

import java.util.List;

import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.repositories.ArtifactVersionRepository;

import org.springframework.beans.factory.annotation.Autowired;

/**
 * Implements custom any custom artifact repository logic.
 */
public class ArtifactVersionRepositoryImpl
    extends GenericVersionRepository<Artifact, ArtifactVersion, ArtifactAppEntity> {

    @Autowired
    ArtifactVersionRepository artifactVersionRepository;

    @Override
    public List<ArtifactVersion> getEntitiesInProject(Project project) {
        return artifactVersionRepository.findByProjectVersionProject(project);
    }

    @Override
    public List<ArtifactVersion> findByEntity(Artifact artifact) {
        return artifactVersionRepository.findByArtifact(artifact);
    }
}
