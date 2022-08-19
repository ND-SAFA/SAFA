package edu.nd.crc.safa.features.delta.entities.app;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * Contains the changes for all versioned entities in a project.
 */
@NoArgsConstructor
@Getter
@Setter
@AllArgsConstructor
public class ProjectDelta {
    EntityDelta<ArtifactAppEntity> artifacts;
    EntityDelta<TraceAppEntity> traces;
}
