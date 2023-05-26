package edu.nd.crc.safa.features.projects.entities.app;

import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

import lombok.Data;

@Data
public class SubtreeAppEntity {
    private Set<UUID> parents;
    private Set<UUID> children;
    private Set<UUID> subtree;
    private Set<UUID> supertree;
    private Set<UUID> neighbors;

    public SubtreeAppEntity() {
        parents = new HashSet<>();
        children = new HashSet<>();
        neighbors = new HashSet<>();
        subtree = new HashSet<>();
        supertree = new HashSet<>();
    }
}
