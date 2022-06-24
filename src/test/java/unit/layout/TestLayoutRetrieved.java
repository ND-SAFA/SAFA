package unit.layout;


import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.Map;

import edu.nd.crc.safa.layout.LayoutPosition;
import edu.nd.crc.safa.layout.LayoutSettings;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;

import org.junit.jupiter.api.Test;

/**
 * Tests that the layout is being returned when retrieving a project.
 */
public class TestLayoutRetrieved extends LayoutBaseTest {

    @Test
    public void testValidLayoutExistsInDefaultProject() throws Exception {
        Map<String, LayoutPosition> layout = project.getLayout();

        // VP - Verify position created for every artifact
        for (ArtifactAppEntity artifact : this.project.artifacts) {
            boolean hasArtifact = layout.containsKey(artifact.id);
            assertThat(hasArtifact).isTrue();
            LayoutPosition artifactPosition = layout.get(artifact.id);
            double x = artifactPosition.getX();
            double y = artifactPosition.getY();
            assertThat(x).isGreaterThan(0);
            assertThat(y).isGreaterThan(0);
        }

        // VP - F1 is at least one node height above F4
        LayoutPosition f1 = layout.get(getArtifactId("F1"));
        LayoutPosition f4 = layout.get(getArtifactId("F4"));

        double deltaY = f4.getY() - f1.getY();
        assertThat(deltaY).isGreaterThan(LayoutSettings.ARTIFACT_HEIGHT);
    }
}
