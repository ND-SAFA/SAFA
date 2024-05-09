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
import edu.nd.crc.safa.features.versions.VersionCalculator;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Responsible for retrieving or creating {@link ArtifactPosition}.
 */
@AllArgsConstructor
@Service
public class ArtifactPositionService {
    private final VersionCalculator versionCalculator = new VersionCalculator();
    private ArtifactPositionRepository artifactPositionRepository;
    private ArtifactRepository artifactRepository;

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
        artifactPositionOptional.ifPresent(position -> artifactPosition.setId(position.getId()));

        // Step 3 - Set position
        artifactPosition.setArtifact(artifact);
        artifactPosition.setProjectVersion(projectVersion);
        artifactPosition.setDocument(document);
        artifactPosition.setX(layoutPosition.getX());
        artifactPosition.setY(layoutPosition.getY());

        return artifactPosition;
    }

    public Map<UUID, LayoutPosition> retrieveDocumentLayout(ProjectVersion projectVersion, UUID documentId) {
        Map<UUID, LayoutPosition> layout = new HashMap<>();
        List<ArtifactPosition> artifactPositionsAcrossVersions = this.artifactPositionRepository
            .getByProjectAndDocumentId(projectVersion.getProject(), documentId);
        Map<UUID, List<ArtifactPosition>> id2pos = ProjectDataStructures.createGroupLookup(
            artifactPositionsAcrossVersions,
            ap -> ap.getArtifact().getArtifactId());
        for (Map.Entry<UUID, List<ArtifactPosition>> entry : id2pos.entrySet()) {
            List<ArtifactPosition> artifactPositions = entry.getValue();
            ArtifactPosition artifactPosition = versionCalculator.getEntityAtVersion(
                artifactPositions,
                projectVersion,
                ArtifactPosition::getProjectVersion);
            if (artifactPosition == null) { // layout for version not available, provide default
                artifactPosition = artifactPositions.get(0);
            }
            LayoutPosition layoutPosition = new LayoutPosition(artifactPosition.getX(), artifactPosition.getY());
            UUID artifactId = artifactPosition.getArtifact().getArtifactId();
            layout.put(artifactId, layoutPosition);
        }

        return layout;
    }
}
