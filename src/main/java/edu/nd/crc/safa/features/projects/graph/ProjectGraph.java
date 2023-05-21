package edu.nd.crc.safa.features.projects.graph;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

public class ProjectGraph {
    Map<UUID, ArtifactNode> artifacts = new HashMap<>();

    public ProjectGraph(ProjectAppEntity projectAppEntity) {
        this.addProjectRelationships(projectAppEntity);
    }

    /**
     * Adds artifacts as nodes and traces as edges.
     *
     * @param projectAppEntity The project entities to create graph from.
     */
    public void addProjectRelationships(ProjectAppEntity projectAppEntity) {
        for (ArtifactAppEntity artifact : projectAppEntity.getArtifacts()) {
            artifacts.put(artifact.getId(), new ArtifactNode(artifact));
        }

        for (TraceAppEntity trace : projectAppEntity.getTraces()) {
            ArtifactNode sourceNode = artifacts.get(trace.getSourceId());
            ArtifactNode targetNode = artifacts.get(trace.getTargetId());
            addRelationship(targetNode, sourceNode);
        }
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
        return artifacts.get(artifactId);
    }
}
