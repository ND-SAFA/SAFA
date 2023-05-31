package edu.nd.crc.safa.features.projects.entities.app;

import java.util.HashSet;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.projects.graph.ArtifactNode;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class SubtreeAppEntity {
    private Set<UUID> parents;
    private Set<UUID> children;
    private Set<UUID> subtree;
    private Set<UUID> supertree;
    private Set<UUID> neighbors;

    public static SubtreeAppEntity fromArtifactNode(ArtifactNode artifactNode) {
        Set<UUID> parents = convertSet(artifactNode.getParents());
        Set<UUID> children = convertSet(artifactNode.getChildren());
        Set<UUID> subtree = convertSet(artifactNode.getSubtree());
        Set<UUID> supertree = convertSet(artifactNode.getSupertree());
        Set<UUID> neighbors = new HashSet<>(subtree);
        neighbors.addAll(supertree);

        return new SubtreeAppEntity(parents, children, subtree, supertree, neighbors);
    }

    private static Set<UUID> convertSet(Set<ArtifactNode> nodeSet) {
        return nodeSet.stream().map(i -> i.getArtifact().getId()).collect(Collectors.toSet());
    }
}
