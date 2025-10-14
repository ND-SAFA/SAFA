package edu.nd.crc.safa.test.features.layout.logic;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.layout.generator.ElkGraphCreator;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.test.common.DefaultProjectConstants;
import edu.nd.crc.safa.test.features.layout.base.AbstractLayoutTest;

import org.eclipse.elk.graph.ElkGraphElement;
import org.eclipse.elk.graph.ElkNode;
import org.javatuples.Pair;
import org.junit.jupiter.api.Test;

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
        String parentName = "F5";
        int nChildren = 0;

        ElkNode d1Node = getArtifact(d1Name);
        List<ElkNode> artifactChildren = getChildren(d1Node);
        ElkNode d1Parent = getParent(d1Node);
        assert d1Parent != null;
        assertThat(d1Parent.getIdentifier()).isEqualTo(getArtifactId(parentName).toString());
        assertThat(artifactChildren).hasSize(nChildren);
    }

    @Test
    void testName2Node() {
        assertThat(name2nodes).hasSize(DefaultProjectConstants.Entities.N_ARTIFACTS);
        for (ArtifactAppEntity artifact : projectAppEntity.getArtifacts()) {
            assertThat(name2nodes).containsKey(artifact.getId());
        }
    }

    @Test
    void testNodeAreChildrenOnGraph() {
        List<String> graphNodesNames = this.rootGraphNode
            .getChildren()
            .stream()
            .map(ElkGraphElement::getIdentifier)
            .collect(Collectors.toList());

        assertThat(graphNodesNames).hasSize(DefaultProjectConstants.Entities.N_ARTIFACTS);
    }

    @Test
    void testChildrenOfTwoArtifactProject() {
        String rootId = "Root";
        UUID r1Id = UUID.randomUUID();
        UUID r2Id = UUID.randomUUID();
        List<UUID> artifactIds = List.of(r1Id, r2Id);
        List<ArtifactAppEntity> artifacts = artifactIds
            .stream()
            .map(this::createArtifact)
            .collect(Collectors.toList());
        List<TraceAppEntity> traces = List.of(createTrace(artifactIds.get(0), artifactIds.get(1)));

        // Create Graph
        Pair<ElkNode, Map<UUID, ElkNode>> result = ElkGraphCreator
            .createGraphFromProject(artifacts, traces);

        // Extract information
        ElkNode graph = result.getValue0();
        graph.setIdentifier(rootId);
        Map<UUID, ElkNode> name2Node = result.getValue1();

        // VP - Verify that root node has correct children
        List<ElkNode> children = graph.getChildren();
        List<String> childrenNames = children
            .stream()
            .map(ElkGraphElement::getIdentifier)
            .collect(Collectors.toList());
        assertThat(children).hasSize(2);
        assertThat(childrenNames).contains(r2Id.toString()).contains(r1Id.toString());

        // VP - Verify that R1 is a child of R2.
        ElkNode parent = getParent(name2Node.get(r1Id));
        assert parent != null;
        assertThat(parent.getIdentifier()).isEqualTo(r2Id.toString());
    }

    private ArtifactAppEntity createArtifact(UUID artifactId) {
        ArtifactAppEntity artifactAppEntity = new ArtifactAppEntity();
        artifactAppEntity.setId(artifactId);
        return artifactAppEntity;
    }

    private TraceAppEntity createTrace(UUID sourceId, UUID targetId) {
        TraceAppEntity traceAppEntity = new TraceAppEntity();
        traceAppEntity.setSourceId(sourceId);
        traceAppEntity.setTargetId(targetId);
        return traceAppEntity;
    }

}
