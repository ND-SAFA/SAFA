package unit.layout;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;

import org.eclipse.elk.graph.ElkGraphElement;
import org.eclipse.elk.graph.ElkNode;
import org.junit.jupiter.api.Test;
import unit.SampleProjectConstants;

/**
 * Tests that creating a graph from a project:
 * 1. Contains all edges present in traces
 * 2. Contains all nodes present as artifacts
 * 3. Number of islands is detected
 * 4. Artifact positions are calculated
 */
public class TestGraphCreation extends LayoutBaseTest {

    @Test
    public void testRootNode() {
        String artifactName = "F1";
        int nChildren = 4; // EA1, F2, F3, F4
        ElkNode artifact = getArtifact(artifactName);

        List<ElkNode> artifactChildren = artifact.getChildren();
        assertThat(artifact.getParent()).isEqualTo(graph);
        assertThat(artifactChildren.size()).isEqualTo(nChildren);
    }

    @Test
    public void testLeafNode() {
        String artifactName = "D1";
        String parentId = "F5";
        int nChildren = 0;

        ElkNode artifact = getArtifact(artifactName);
        List<ElkNode> artifactChildren = artifact.getChildren();
        assertThat(artifact.getParent().getIdentifier()).isEqualTo(getArtifactId(parentId));
        assertThat(artifactChildren.size()).isEqualTo(nChildren);
    }

    @Test
    public void testName2Node() {
        assertThat(name2nodes.size()).isEqualTo(SampleProjectConstants.N_ARTIFACTS);
        for (ArtifactAppEntity artifact : project.getArtifacts()) {
            assertThat(name2nodes.containsKey(artifact.id)).isTrue();
        }
    }

    @Test
    public void rootNode() {
        List<String> rootNodeNames = this.graph
            .getChildren()
            .stream()
            .map(ElkGraphElement::getIdentifier)
            .collect(Collectors.toList());


        assertThat(rootNodeNames.contains(getArtifactId("F1"))).isTrue();
        assertThat(rootNodeNames.contains(getArtifactId("D10"))).isTrue();
        assertThat(rootNodeNames.contains(getArtifactId("D11"))).isTrue();
        assertThat(rootNodeNames.size()).isEqualTo(3);
    }
}
