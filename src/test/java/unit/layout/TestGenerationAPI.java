package unit.layout;


import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.Map;

import edu.nd.crc.safa.layout.LayoutPosition;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;

import org.junit.jupiter.api.Test;

public class TestGenerationAPI extends LayoutBaseTest {

    @Test
    public void getLayoutForDefaultProject() throws Exception {
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
    }
}
