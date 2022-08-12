package edu.nd.crc.safa.features.layout.services;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
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
    ArtifactRepository artifactRepository;

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

        // Step - 1 Retrieve artifact
        String artifactName = artifactAppEntity.getName();
        Optional<Artifact> artifactOptional = this.artifactRepository.findByProjectAndName(projectVersion.getProject(),
            artifactName);
        if (artifactOptional.isEmpty()) {
            throw new IllegalArgumentException("Could not find artifact with name:" + artifactName);
        }
        Artifact artifact = artifactOptional.get();

        // Step 2 - Check if position has already been created or set properties
        UUID documentId = document == null ? null : document.getDocumentId();
        Optional<ArtifactPosition> artifactPositionOptional =
            artifactPositionRepository.findByProjectVersionAndArtifactAndDocumentDocumentId(
                projectVersion, artifact, documentId);
        if (artifactPositionOptional.isPresent()) {
            artifactPosition = artifactPositionOptional.get();
        } else {
            // Step 2 - Set properties document
            artifactPosition.setArtifact(artifact);
            artifactPosition.setProjectVersion(projectVersion);
            artifactPosition.setDocument(document);
        }

        // Step 3 - Set position
        artifactPosition.setX(layoutPosition.getX());
        artifactPosition.setY(layoutPosition.getY());

        return artifactPosition;
    }

    public Map<String, LayoutPosition> retrieveDocumentLayout(UUID documentId) {
        Map<String, LayoutPosition> layout = new HashMap<>();
        List<ArtifactPosition> artifactPositions = this.artifactPositionRepository.findByDocumentDocumentId(documentId);
        for (ArtifactPosition artifactPosition : artifactPositions) {
            String artifactId = artifactPosition.getArtifact().getArtifactId().toString();
            LayoutPosition layoutPosition = new LayoutPosition(artifactPosition.getX(), artifactPosition.getY());
            layout.put(artifactId, layoutPosition);
        }
        return layout;
    }
}
