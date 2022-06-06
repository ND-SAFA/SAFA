package edu.nd.crc.safa.layout;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ApprovalStatus;

import org.eclipse.elk.core.math.KVector;
import org.eclipse.elk.core.options.CoreOptions;
import org.eclipse.elk.graph.ElkGraphFactory;
import org.eclipse.elk.graph.ElkNode;
import org.javatuples.Pair;

/**
 * Responsible for creating an elk graph from a project app entity.
 */
public class ElkGraphCreator {

    static ElkGraphFactory factory = ElkGraphFactory.eINSTANCE;

    public static Pair<ElkNode, Hashtable<String, ElkNode>> createGraphFromProject(ProjectAppEntity projectAppEntity) {
        Hashtable<String, ElkNode> name2node = createName2ElkNode(projectAppEntity.artifacts);
        connectNodesWithTraces(name2node, projectAppEntity.traces);

        ElkNode graph = createNode();
        List<ElkNode> nodes = new ArrayList<>(name2node.values());
        List<ElkNode> rootNodes = getRootNodes(nodes);

        for (ElkNode rootNode : rootNodes) {
            rootNode.setParent(graph);
        }
        return new Pair<>(graph, name2node);
    }

    public static Hashtable<String, ElkNode> createName2ElkNode(List<ArtifactAppEntity> artifacts) {
        Hashtable<String, ElkNode> nodes = new Hashtable<>();
        for (ArtifactAppEntity artifact : artifacts) {
            nodes.put(artifact.name, createElkNodeFromArtifact(artifact));
        }
        return nodes;
    }

    private static ElkNode createElkNodeFromArtifact(ArtifactAppEntity artifact) {
        ElkNode elkNode = createNode();
        elkNode.setIdentifier(artifact.name);
        return elkNode;
    }

    public static void connectNodesWithTraces(Hashtable<String, ElkNode> name2node,
                                              List<TraceAppEntity> traces) {
        traces
            .stream()
            .filter(t -> t.getApprovalStatus() == ApprovalStatus.APPROVED)
            .forEach(t -> {
                ElkNode sourceNode = name2node.get(t.sourceName);
                ElkNode targetNode = name2node.get(t.targetName);
                sourceNode.setParent(targetNode);
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
        elkNode.setProperty(CoreOptions.ALGORITHM, LayoutSettings.LAYOUT_ALGORITHM);
        //.setProperty(CoreOptions.HIERARCHY_HANDLING, INCLUDE_CHILDREN)
        elkNode.setProperty(CoreOptions.NODE_SIZE_MINIMUM, new KVector(
            LayoutSettings.ARTIFACT_WIDTH,
            LayoutSettings.ARTIFACT_HEIGHT));

        return elkNode;
    }
}
