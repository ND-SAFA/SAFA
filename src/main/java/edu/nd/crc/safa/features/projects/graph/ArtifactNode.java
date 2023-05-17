package edu.nd.crc.safa.features.projects.graph;

import java.util.ArrayList;
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

    ArtifactAppEntity artifact;
    List<ArtifactNode> neighbors = new ArrayList<>();
    List<ArtifactNode> parents = new ArrayList<>();
    List<ArtifactNode> children = new ArrayList<>();

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
        this.parents.add(childNode);
    }

    /**
     * Calculates artifacts in neighborhood containing types.
     *
     * @param artifactTypes Types of artifacts to include in calculation.
     * @return Artifact IDs in neighborhoods.
     */
    public List<UUID> getNeighborhoodWithTypes(Set<String> artifactTypes) {
        List<UUID> neighborhoodWithTypes = new ArrayList<>();
        neighborhoodWithTypes.add(artifact.getId());
        this.addNeighborhoodNodesWithTypes(artifactTypes, neighborhoodWithTypes);
        neighborhoodWithTypes.remove(artifact.getId());
        return neighborhoodWithTypes;
    }

    private void addNeighborhoodNodesWithTypes(Set<String> artifactTypes, List<UUID> artifactsSeen) {
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
