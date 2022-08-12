package edu.nd.crc.safa.features.layout.services;

import java.util.Optional;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.layout.entities.db.ArtifactPosition;
import edu.nd.crc.safa.features.layout.repositories.ArtifactPositionRepository;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Responsible for retrieving or creating {@link ArtifactPosition}.
 */
@AllArgsConstructor
@Service
public class ArtifactPositionService {
    ArtifactPositionRepository artifactPositionRepository;
    ArtifactVersionRepository artifactVersionRepository;

    /**
     * Creates or updates artifact position within document using artifact version id and given document.
     *
     * @param projectVersion    Project version associated with artifact version to set position of.
     * @param artifactAppEntity The artifact whose version is extracted.
     * @param layoutPosition    The new position to update to.
     * @param document          The document whose position we are updating.
     * @return {@link ArtifactPosition} The position of artifact within document tree.
     */
    public ArtifactPosition createOrUpdateArtifactPosition(ProjectVersion projectVersion,
                                                           ArtifactAppEntity artifactAppEntity,
                                                           LayoutPosition layoutPosition,
                                                           Document document) {
        ArtifactPosition artifactPosition = new ArtifactPosition();

        // Step 1 - Retrieve artifact version
        Optional<ArtifactVersion> artifactVersionOptional = artifactVersionRepository
            .findByProjectVersionAndArtifactName(projectVersion, artifactAppEntity.name);
        assert artifactVersionOptional.isPresent();
        ArtifactVersion artifactVersion = artifactVersionOptional.get();

        // Step 2 - Check if position has already been created or set properties
        Optional<ArtifactPosition> artifactPositionOptional =
            artifactPositionRepository.findByArtifactVersionAndDocument(artifactVersion,
                document);
        if (artifactPositionOptional.isPresent()) {
            artifactPosition = artifactPositionOptional.get();
        } else {
            // Step 2 - Set properties document
            artifactPosition.setArtifactVersion(artifactVersion);
            artifactPosition.setDocument(document);
        }
        
        // Step 3 - Set position
        artifactPosition.setX(layoutPosition.getX());
        artifactPosition.setY(layoutPosition.getY());

        return artifactPosition;
    }
}
