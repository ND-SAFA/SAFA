package edu.nd.crc.safa.server.entities.app.delta;

import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;

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
