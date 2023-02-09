package edu.nd.crc.safa.test.services;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;

/**
 * Container for verification of layout methods.
 */
public class LayoutTestService {

    /**
     * Verifies that all layouts have non-zero values.
     *
     * @param project Project whose documents layouts are being checked.
     */
    public void verifyProjectLayout(ProjectAppEntity project) {
        verifyLayout(project.getLayout(),
            project
                .getArtifacts()
                .stream()
                .map(ArtifactAppEntity::getId)
                .collect(Collectors.toList()));
        for (DocumentAppEntity documentAppEntity : project.getDocuments()) {
            verifyLayout(documentAppEntity.getLayout(), documentAppEntity.getArtifactIds());
        }
    }

    /**
     * Verfies that layout contains non-zero values and has a position for each given artifact ID.
     *
     * @param layout      The layout to check for non-zero values.
     * @param artifactIds The ID to verify have positions.
     */
    public void verifyLayout(Map<UUID, LayoutPosition> layout, List<UUID> artifactIds) {
        assertThat(layout).size().isGreaterThanOrEqualTo(artifactIds.size());
        for (UUID artifactId : artifactIds) {
            assertThat(layout.get(artifactId))
                .as("artifact id has layout:" + artifactId)
                .isNotNull();
        }
    }
}
