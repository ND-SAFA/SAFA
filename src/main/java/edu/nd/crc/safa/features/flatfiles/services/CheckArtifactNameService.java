package edu.nd.crc.safa.features.flatfiles.services;

import java.util.Optional;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.flatfiles.entities.app.ArtifactNameCheck;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

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
            String artifactId = artifactQuery.get().getArtifactId().toString();
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
