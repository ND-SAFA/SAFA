package edu.nd.crc.safa.features.projects.graph;

import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.Set;
import java.util.UUID;
import java.util.function.Function;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SubtreeAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;

public class ProjectGraph {
    private Map<UUID, ArtifactNode> artifactsMap = new HashMap<>();

    public ProjectGraph(ProjectAppEntity projectAppEntity) {
        this.addProjectRelationships(projectAppEntity.getArtifacts(), projectAppEntity.getTraces());
    }

    public ProjectGraph(ProjectEntities projectEntities) {
        this.addProjectRelationships(projectEntities.getArtifacts(), projectEntities.getTraces());
    }

    /**
     * Adds artifacts as nodes and traces as edges.
     *
     * @param artifacts The project artifacts to create graph from.
     * @param traces    The project traces to create graph from.
     */
    public void addProjectRelationships(List<ArtifactAppEntity> artifacts, List<TraceAppEntity> traces) {
        for (ArtifactAppEntity artifact : artifacts) {
            artifactsMap.put(artifact.getId(), new ArtifactNode(artifact));
        }

        for (TraceAppEntity trace : traces) {
            if (traceLinkIsVisible(trace)) {
                ArtifactNode sourceNode = artifactsMap.get(trace.getSourceId());
                ArtifactNode targetNode = artifactsMap.get(trace.getTargetId());
                if (sourceNode == null || targetNode == null) {
                    continue;
                }
                addRelationship(targetNode, sourceNode);
            }
        }

        for (ArtifactNode item : artifactsMap.values()) {
            calculateSingleSubtree(item);
            calculateSingleSupertree(item);
        }
    }

    /**
     * Return whether a trace link should be displayed
     *
     * @param trace The trace link
     * @return Whether we should display the trace
     */
    private boolean traceLinkIsVisible(TraceAppEntity trace) {
        return trace.isVisible()
            && (trace.getTraceType() == TraceType.MANUAL || trace.getApprovalStatus() != ApprovalStatus.DECLINED);
    }

    /**
     * Adds edge between parent and child.
     *
     * @param parent The parent node.
     * @param child  The child node.
     */
    public void addRelationship(ArtifactNode parent, ArtifactNode child) {
        child.addParent(parent);
        parent.addChild(child);
    }

    /**
     * The artifact node by ID.
     *
     * @param artifactId The artifact ID of the node to retrieve.
     * @return The artifact node with ID.
     */
    public ArtifactNode getArtifactNode(UUID artifactId) {
        return artifactsMap.get(artifactId);
    }

    /**
     * Broadcasts this item into a supertree/subtree set all the way up/down its reachability chain.
     *
     * @param item               Item we are processing.
     * @param subtreeRetriever   Function which will grab the supertree/subtree set from the app entity.
     * @param nextItemsRetriever Function which will grab the parent/children set from the app entity.
     */
    private void broadcastTreeMembership(ArtifactNode item,
                                         Function<ArtifactNode, Set<ArtifactNode>> subtreeRetriever,
                                         Function<ArtifactNode, Set<ArtifactNode>> nextItemsRetriever) {

        Queue<ArtifactNode> itemsToVisit = new LinkedList<>();
        itemsToVisit.add(item);

        Set<UUID> visited = new HashSet<>();

        while (!itemsToVisit.isEmpty()) {
            ArtifactNode currentItem = itemsToVisit.poll();
            visited.add(currentItem.getArtifact().getId());

            subtreeRetriever.apply(currentItem).add(item);

            for (ArtifactNode nextId : nextItemsRetriever.apply(currentItem)) {
                if (!visited.contains(nextId.getArtifact().getId())) {
                    itemsToVisit.add(nextId);
                }
            }
        }

        subtreeRetriever.apply(item).remove(item);
    }

    /**
     * Calculates subtree information for this item by adding it to all of its ancestors' subtree sets.
     *
     * @param item The item we are processing.
     */
    private void calculateSingleSubtree(ArtifactNode item) {
        broadcastTreeMembership(item, ArtifactNode::getSubtree, ArtifactNode::getParents);
    }

    /**
     * Calculates supertree information for this item by adding it to all of its descendants' supertree sets.
     *
     * @param item The item we are processing.
     */
    private void calculateSingleSupertree(ArtifactNode item) {
        broadcastTreeMembership(item, ArtifactNode::getSupertree, ArtifactNode::getChildren);
    }

    /**
     * Get subtree information for the front end.
     *
     * @return Subtree information for this project
     */
    public Map<UUID, SubtreeAppEntity> getSubtreeInfo() {
        Map<UUID, SubtreeAppEntity> out = new HashMap<>();
        for (UUID id : artifactsMap.keySet()) {
            out.put(id, SubtreeAppEntity.fromArtifactNode(artifactsMap.get(id)));
        }
        return out;
    }
}
