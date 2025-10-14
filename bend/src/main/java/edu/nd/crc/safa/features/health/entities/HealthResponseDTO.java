package edu.nd.crc.safa.features.health.entities;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.UUID;

import edu.nd.crc.safa.features.comments.entities.dtos.comments.CommentDTO;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class HealthResponseDTO {
    /**
     * List of health checks related to an artifact.
     */
    private List<CommentDTO> healthChecks = new ArrayList<>();

    /**
     * Adds new checks to health checks.
     *
     * @param newChecks New checks to add.
     * @param <T>       Type of comment being added.
     */
    public <T extends CommentDTO> void addHealthChecks(List<T> newChecks) {
        this.healthChecks.addAll(newChecks);
    }

    /**
     * Creates new response object containing only the health checks regarding artifact id.
     *
     * @param artifactIds Artifact Ids to whose health checks are kept.
     * @return HealthResponse with filtered health checks.
     */
    public HealthResponseDTO filterById(List<UUID> artifactIds) {
        Set<UUID> artifactIdSet = new HashSet<>(artifactIds);
        List<CommentDTO> filteredHealthChecks =
            this.healthChecks.stream().filter(h -> artifactIdSet.contains(h.getArtifactId())).toList();
        return new HealthResponseDTO(filteredHealthChecks);
    }
}
