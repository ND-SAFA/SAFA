package edu.nd.crc.safa.features.projects.graph;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;

import lombok.Getter;

/**
 * Represents an artifact node in a graph.
 */
@Getter
public class ArtifactNode {

    private final ArtifactAppEntity artifact;
    private final Set<ArtifactNode> neighbors = new HashSet<>();
    private final Set<ArtifactNode> parents = new HashSet<>();
    private final Set<ArtifactNode> children = new HashSet<>();
    private final Set<ArtifactNode> subtree = new HashSet<>();
    private final Set<ArtifactNode> supertree = new HashSet<>();

    public ArtifactNode(ArtifactAppEntity artifact) {
        this.artifact = artifact;
    }

    /**
     * Adds node as parent.
     *
     * @param parentNode Artifact node to store as parent and neighbor.
     */
    public void addParent(ArtifactNode parentNode) {
        this.neighbors.add(parentNode);
        this.parents.add(parentNode);
    }

    /**
     * Adds node as child.
     *
     * @param childNode Artifact node to store as child and neighbor.
     */
    public void addChild(ArtifactNode childNode) {
        this.neighbors.add(childNode);
        this.children.add(childNode);
    }

    /**
     * Calculates artifacts in neighborhood containing types.
     *
     * @param artifactTypes Types of artifacts to include in calculation.
     * @return Artifact IDs in neighborhoods.
     */
    public List<UUID> getNeighborhoodWithTypes(Set<String> artifactTypes) {
        Set<UUID> neighborhoodWithTypes = new HashSet<>();
        neighborhoodWithTypes.add(artifact.getId());
        this.addNeighborhoodNodesWithTypes(artifactTypes, neighborhoodWithTypes);
        neighborhoodWithTypes.remove(artifact.getId());
        return new ArrayList<>(neighborhoodWithTypes);
    }

    private void addNeighborhoodNodesWithTypes(Set<String> artifactTypes, Set<UUID> artifactsSeen) {
        for (ArtifactNode artifactNode : neighbors) {
            UUID artifactId = artifactNode.artifact.getId();
            String artifactNodeType = artifactNode.artifact.getType();
            if (!artifactsSeen.contains(artifactId) && artifactTypes.contains(artifactNodeType)) {
                artifactsSeen.add(artifactId);
                artifactNode.addNeighborhoodNodesWithTypes(artifactTypes, artifactsSeen);
            }
        }
    }
}
