package edu.nd.crc.safa.features.flatfiles.services;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactVersion;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
import edu.nd.crc.safa.features.artifacts.repositories.versions.ArtifactVersionRepository;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.flatfiles.controllers.entities.ArtifactNameCheck;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Responsible for checking if some artifact is present in
 * specified project versions.
 */
@Service
@AllArgsConstructor
public class CheckArtifactNameService {
    ArtifactRepository artifactRepository;
    ArtifactVersionRepository artifactVersionRepository;

    public boolean doesArtifactExist(
        ProjectVersion projectVersion,
        ArtifactNameCheck artifactNameCheck
    ) {
        Optional<Artifact> artifactQuery =
            this.artifactRepository.findByProjectAndName(projectVersion.getProject(),
                artifactNameCheck.getArtifactName());
        boolean artifactExists = false;
        if (artifactQuery.isPresent()) {
            UUID artifactId = artifactQuery.get().getArtifactId();
            Optional<ArtifactVersion> artifactVersionQuery =
                this.artifactVersionRepository.findVersionEntityByProjectVersionAndBaseEntityId(
                    projectVersion,
                    artifactId);
            if (artifactVersionQuery.isPresent()) {
                artifactExists = !artifactVersionQuery.get().getModificationType().equals(ModificationType.REMOVED);
            }
        }
        return artifactExists;
    }
}
