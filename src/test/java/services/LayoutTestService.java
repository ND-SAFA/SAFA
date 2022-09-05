package services;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;

/**
 * Container for verification of layout methods.
 */
public class LayoutTestService {

    /**
     * Verifies that each artifact contains a non-zero layout position.
     *
     * @param layout      The layout to verify.
     * @param artifactIds The artifact IDs expected to be present in layout.
     */
    public void verifyLayout(Map<UUID, LayoutPosition> layout, List<UUID> artifactIds) {
        assertThat(layout).hasSize(artifactIds.size());
        for (UUID artifactId : artifactIds) {
            assertThat(layout.get(artifactId))
                .as("artifact id has layout:" + artifactId)
                .isNotNull();
        }
    }
}
