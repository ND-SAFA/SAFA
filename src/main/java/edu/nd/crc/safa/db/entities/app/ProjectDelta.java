package edu.nd.crc.safa.db.entities.app;

import java.util.List;

public class ProjectDelta {
    List<AddedArtifact> added;
    List<ModifiedArtifact> modified;
    List<RemovedArtifact> removed;

    public ProjectDelta() {
    }

    public ProjectDelta(List<AddedArtifact> added,
                        List<ModifiedArtifact> modified,
                        List<RemovedArtifact> removed) {
        this.added = added;
        this.modified = modified;
        this.removed = removed;
    }

    public List<AddedArtifact> getAdded() {
        return this.added;
    }

    public void setAdded(List<AddedArtifact> added) {
        this.added = added;
    }

    public List<ModifiedArtifact> getModified() {
        return this.modified;
    }

    public void setModified(List<ModifiedArtifact> modified) {
        this.modified = modified;
    }

    public List<RemovedArtifact> getRemoved() {
        return this.removed;
    }

    public void setRemoved(List<RemovedArtifact> removed) {
        this.removed = removed;
    }
}
