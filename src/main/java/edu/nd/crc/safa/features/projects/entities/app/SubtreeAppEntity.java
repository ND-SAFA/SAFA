package edu.nd.crc.safa.features.projects.entities.app;

import java.util.List;
import java.util.UUID;

import lombok.Data;
import net.minidev.json.annotate.JsonIgnore;

@Data
public class SubtreeAppEntity {
    private List<UUID> parents;
    private List<UUID> children;
    private List<UUID> subtree;
    @JsonIgnore private List<UUID> supertree;
    private List<UUID> neighbors;
}
