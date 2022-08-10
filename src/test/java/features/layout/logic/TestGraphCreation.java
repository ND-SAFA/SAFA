package features.layout.logic;


import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.layout.generator.ElkGraphCreator;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import features.layout.base.AbstractLayoutTest;
import org.eclipse.elk.graph.ElkGraphElement;
import org.eclipse.elk.graph.ElkNode;
import org.javatuples.Pair;
import org.junit.jupiter.api.Test;
import features.base.DefaultProjectConstants;

/**
 * Tests that creating a graph from a project:
 * 1. Contains all edges present in traces
 * 2. Contains all nodes present as artifacts
 * 3. Number of islands is detected
 * 4. Artifact positions are calculated
 */
class TestGraphCreation extends AbstractLayoutTest {

    @Test
    void testInternalMethods() {
        String d1Name = "D1";
        String parentId = "F5";
        int nChildren = 0;

        ElkNode d1Node = getArtifact(d1Name);
        List<ElkNode> artifactChildren = getChildren(d1Node);
        ElkNode d1Parent = getParent(d1Node);
        assert d1Parent != null;
        assertThat(d1Parent.getIdentifier()).isEqualTo(getArtifactId(parentId));
        assertThat(artifactChildren.size()).isEqualTo(nChildren);
    }

    @Test
    void testName2Node() {
        assertThat(name2nodes).hasSize(DefaultProjectConstants.Entities.N_ARTIFACTS);
        for (ArtifactAppEntity artifact : project.getArtifacts()) {
            assertThat(name2nodes).containsKey(artifact.id);
        }
    }

    @Test
    void testNodeAreChildrenOnGraph() {
        List<String> graphNodesNames = this.rootGraphNode
            .getChildren()
            .stream()
            .map(ElkGraphElement::getIdentifier)
            .collect(Collectors.toList());

        assertThat(graphNodesNames.size()).isEqualTo(DefaultProjectConstants.Entities.N_ARTIFACTS);
    }

    @Test
    void testChildrenOfTwoArtifactProject() {
        String rootId = "Root";
        List<String> artifactIds = List.of("R1", "R2");
        List<ArtifactAppEntity> artifacts = artifactIds
            .stream()
            .map(this::createArtifact)
            .collect(Collectors.toList());
        List<TraceAppEntity> traces = List.of(createTrace(artifactIds.get(0), artifactIds.get(1)));

        // Create Graph
        Pair<ElkNode, Map<String, ElkNode>> result = ElkGraphCreator
            .createGraphFromProject(artifacts, traces);

        // Extract information
        ElkNode graph = result.getValue0();
        graph.setIdentifier(rootId);
        Map<String, ElkNode> name2Node = result.getValue1();

        // VP - Verify that root node has correct children
        List<ElkNode> children = graph.getChildren();
        List<String> childrenNames = children
            .stream()
            .map(ElkGraphElement::getIdentifier)
            .collect(Collectors.toList());
        assertThat(children.size()).isEqualTo(2);
        assertThat(childrenNames.contains("R2")).isTrue();
        assertThat(childrenNames.contains("R1")).isTrue();

        // VP - Verify that R1 is a child of R2.
        ElkNode parent = getParent(name2Node.get("R1"));
        assert parent != null;
        assertThat(parent.getIdentifier()).isEqualTo("R2");
    }

    private ArtifactAppEntity createArtifact(String artifactName) {
        ArtifactAppEntity artifactAppEntity = new ArtifactAppEntity();
        artifactAppEntity.setId(artifactName);
        return artifactAppEntity;
    }

    private TraceAppEntity createTrace(String sourceName, String targetName) {
        TraceAppEntity traceAppEntity = new TraceAppEntity();
        traceAppEntity.setSourceId(sourceName);
        traceAppEntity.setTargetId(targetName);
        return traceAppEntity;
    }

}
