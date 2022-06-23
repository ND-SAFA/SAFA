package edu.nd.crc.safa.layout;

import static edu.nd.crc.safa.layout.LayoutSettings.LAYOUT_ALGORITHM;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ApprovalStatus;

import org.eclipse.elk.core.options.CoreOptions;
import org.eclipse.elk.graph.ElkConnectableShape;
import org.eclipse.elk.graph.ElkEdge;
import org.eclipse.elk.graph.ElkGraphFactory;
import org.eclipse.elk.graph.ElkNode;
import org.eclipse.elk.graph.util.ElkGraphUtil;
import org.javatuples.Pair;

/**
 * Responsible for creating an elk graph from a project app entity.
 */
public class ElkGraphCreator {

    static ElkGraphFactory factory = ElkGraphFactory.eINSTANCE;

    public static Pair<ElkNode, Hashtable<String, ElkNode>> createGraphFromProject(
        List<ArtifactAppEntity> artifacts,
        List<TraceAppEntity> traces
    ) {
        Hashtable<String, ElkNode> name2node = createName2ElkNode(artifacts);
        connectNodesWithTraces(name2node, traces);
        ElkNode graph = connectToRootNode(getNodes(name2node));
        return new Pair<>(graph, name2node);
    }

    private static ElkNode connectToRootNode(List<ElkNode> nodes) {
        ElkNode graph = createNode();
        getRootNodes(nodes).forEach((rootNode) -> rootNode.setParent(graph));
        return graph;
    }

    public static List<ElkNode> getNodes(Hashtable<String, ElkNode> name2node) {
        return new ArrayList<>(name2node.values());
    }

    public static Hashtable<String, ElkNode> createName2ElkNode(List<ArtifactAppEntity> artifacts) {
        Hashtable<String, ElkNode> nodes = new Hashtable<>();
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

    public static void connectNodesWithTraces(Hashtable<String, ElkNode> name2node,
                                              List<TraceAppEntity> traces) {
        traces
            .stream()
            .filter(t -> t.getApprovalStatus() != ApprovalStatus.DECLINED)
            .forEach(t -> {
                ElkNode sourceNode = name2node.get(t.sourceId);
                ElkNode targetNode = name2node.get(t.targetId);

                ElkGraphUtil.createSimpleEdge(targetNode, sourceNode);
            });
    }

    public static List<ElkNode> getRootNodes(List<ElkNode> nodes) {
        Hashtable<String, ElkNode> rootNodes = new Hashtable<>();
        for (ElkNode node : nodes) {
            ElkNode rootNode = getRootNode(node);
            String rootNodeId = rootNode.getIdentifier();
            if (!rootNodes.containsKey(rootNodeId)) {
                rootNodes.put(rootNodeId, rootNode);
            }
        }
        return new ArrayList<>(rootNodes.values());
    }

    public static ElkNode getRootNode(ElkNode elkNode) {
        if (elkNode.getParent() == null) {
            return elkNode;
        } else {
            return getRootNode(elkNode.getParent());
        }
    }

    private static ElkNode createNode() {
        ElkNode elkNode = factory.createElkNode();

        elkNode.setDimensions(LayoutSettings.ARTIFACT_WIDTH, LayoutSettings.ARTIFACT_HEIGHT);
        elkNode.setProperty(CoreOptions.ALGORITHM, LAYOUT_ALGORITHM);

        return elkNode;
    }
}
