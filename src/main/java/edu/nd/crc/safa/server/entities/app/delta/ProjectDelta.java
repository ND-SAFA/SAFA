package edu.nd.crc.safa.server.entities.app.delta;

import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;

/**
 * Contains the changes for all versioned entities in a project.
 */
public class ProjectDelta {
    EntityDelta<ArtifactAppEntity> artifacts;
    EntityDelta<TraceAppEntity> traces;

    public ProjectDelta(EntityDelta<ArtifactAppEntity> artifacts,
                        EntityDelta<TraceAppEntity> traces) {
        this.artifacts = artifacts;
        this.traces = traces;
    }

    public EntityDelta<ArtifactAppEntity> getArtifacts() {
        return artifacts;
    }

    public void setArtifacts(EntityDelta<ArtifactAppEntity> artifacts) {
        this.artifacts = artifacts;
    }

    public EntityDelta<TraceAppEntity> getTraces() {
        return traces;
    }

    public void setTraces(EntityDelta<TraceAppEntity> traces) {
        this.traces = traces;
    }
}
