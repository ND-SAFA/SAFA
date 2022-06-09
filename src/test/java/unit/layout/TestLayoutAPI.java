package unit.layout;


import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;

import org.eclipse.elk.graph.ElkNode;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

public class TestLayoutAPI extends LayoutBaseTest {

    @Test
    public void getLayoutForDefaultProject() throws Exception {
        String route = RouteBuilder
            .withRoute(AppRoutes.Projects.Layout.createLayoutForProject)
            .withVersion(this.projectVersion)
            .get();
        JSONObject layout = sendPost(route, new JSONObject());

        // VP - Verify position created for every artifact
        for (ArtifactAppEntity artifact : this.project.artifacts) {
            boolean hasArtifact = layout.has(artifact.id);
            assertThat(hasArtifact).isTrue();
            JSONObject artifactPosition = layout.getJSONObject(artifact.id);
            double x = artifactPosition.getNumber("x").doubleValue();
            double y = artifactPosition.getNumber("y").doubleValue();
            assertThat(x).isGreaterThanOrEqualTo(0);
        }
    }

    public void printGraph(int level, ElkNode node) {
        System.out.println(level + ":" + node);
        for (ElkNode child : node.getChildren()) {
            printGraph(level + 1, child);
        }
    }
}
