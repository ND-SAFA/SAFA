package edu.nd.crc.safa.features.health.entities;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.comments.entities.dtos.comments.CommentDTO;

import lombok.Data;

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
}
