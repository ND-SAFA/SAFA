package edu.nd.crc.safa.features.health;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.comments.entities.dtos.comments.CommentDTO;

import lombok.Data;

@Data
public class HealthResponse {
    /**
     * List of health checks related to an artifact.
     */
    private List<CommentDTO> healthChecks = new ArrayList<>();

    /**
     * Adds new checks to health checks.
     *
     * @param newChecks New checks to add.
     */
    public <T extends CommentDTO> void addHealthChecks(List<T> newChecks) {
        this.healthChecks.addAll(newChecks);
    }
}
