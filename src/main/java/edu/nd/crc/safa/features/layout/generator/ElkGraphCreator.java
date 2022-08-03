package edu.nd.crc.safa.features.layout.generator;

import static edu.nd.crc.safa.features.layout.LayoutSettings.LAYOUT_ALGORITHM;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.layout.LayoutSettings;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.eclipse.elk.core.options.CoreOptions;
import org.eclipse.elk.graph.ElkGraphFactory;
import org.eclipse.elk.graph.ElkNode;
import org.eclipse.elk.graph.util.ElkGraphUtil;
import org.javatuples.Pair;

/**
 * Responsible for creating an elk graph from a project app entity.
 */
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class ElkGraphCreator {

    static ElkGraphFactory factory = ElkGraphFactory.eINSTANCE;

    public static Pair<ElkNode, Map<String, ElkNode>> createGraphFromProject(
        List<ArtifactAppEntity> artifacts,
        List<TraceAppEntity> traces
    ) {
        Map<String, ElkNode> name2node = createName2ElkNode(artifacts);
        connectNodesWithTraces(name2node, traces);
        ElkNode graph = connectToRootNode(getNodes(name2node));
        return new Pair<>(graph, name2node);
    }

    private static ElkNode connectToRootNode(List<ElkNode> nodes) {
        ElkNode graph = createNode();
        nodes.forEach(n -> n.setParent(graph));
        return graph;
    }

    public static List<ElkNode> getNodes(Map<String, ElkNode> name2node) {
        return new ArrayList<>(name2node.values());
    }

    public static Map<String, ElkNode> createName2ElkNode(List<ArtifactAppEntity> artifacts) {
        Map<String, ElkNode> nodes = new HashMap<>();
        for (ArtifactAppEntity artifact : artifacts) {
            nodes.put(artifact.id, createElkNodeFromArtifact(artifact));
        }
        return nodes;
    }

    private static ElkNode createElkNodeFromArtifact(ArtifactAppEntity artifact) {
        ElkNode elkNode = createNode();
        elkNode.setIdentifier(artifact.id);
        return elkNode;
    }

    public static void connectNodesWithTraces(Map<String, ElkNode> name2node,
                                              List<TraceAppEntity> traces) {
        traces
            .stream()
            .filter(t -> t.getApprovalStatus() != ApprovalStatus.DECLINED)
            .forEach(t -> {
                ElkNode sourceNode = name2node.get(t.getSourceId());
                ElkNode targetNode = name2node.get(t.getTargetId());

                ElkGraphUtil.createSimpleEdge(targetNode, sourceNode);
            });
    }

    private static ElkNode createNode() {
        ElkNode elkNode = factory.createElkNode();

        elkNode.setDimensions(LayoutSettings.ARTIFACT_WIDTH, LayoutSettings.ARTIFACT_HEIGHT);
        elkNode.setProperty(CoreOptions.ALGORITHM, LAYOUT_ALGORITHM);

        return elkNode;
    }
}
