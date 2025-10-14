package edu.nd.crc.safa.test.features.layout.crud;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.layout.LayoutSettings;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.test.features.layout.base.AbstractLayoutTest;

import org.junit.jupiter.api.Test;

/**
 * Tests that the layout is being returned when retrieving a project.
 */
class TestLayoutRetrieved extends AbstractLayoutTest {

    @Test
    void testValidLayoutExistsInDefaultProject() {
        Map<UUID, LayoutPosition> layout = projectAppEntity.getLayout();

        // VP - Verify position created for every artifact
        for (ArtifactAppEntity artifact : this.projectAppEntity.getArtifacts()) {
            boolean hasArtifact = layout.containsKey(artifact.getId());
            assertThat(hasArtifact).isTrue();
            LayoutPosition artifactPosition = layout.get(artifact.getId());
            double x = artifactPosition.getX();
            double y = artifactPosition.getY();
            assertThat(x).isPositive();
            assertThat(y).isPositive();
        }

        // VP - F1 is at least one node height above F4
        LayoutPosition f1 = layout.get(getArtifactId("F1"));
        LayoutPosition f4 = layout.get(getArtifactId("F4"));

        double deltaY = f4.getY() - f1.getY();
        assertThat(deltaY).isGreaterThan(LayoutSettings.ARTIFACT_HEIGHT);
    }
}
