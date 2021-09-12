package edu.nd.crc.safa.server.db.entities.app;

import java.util.Hashtable;

public class ProjectDelta {
    Hashtable<String, AddedArtifact> added;
    Hashtable<String, ModifiedArtifact> modified;
    Hashtable<String, RemovedArtifact> removed;

    public ProjectDelta() {
    }

    public ProjectDelta(Hashtable<String, AddedArtifact> added,
                        Hashtable<String, ModifiedArtifact> modified,
                        Hashtable<String, RemovedArtifact> removed) {
        this.added = added;
        this.modified = modified;
        this.removed = removed;
    }

    public Hashtable<String, AddedArtifact> getAdded() {
        return this.added;
    }

    public void setAdded(Hashtable<String, AddedArtifact> added) {
        this.added = added;
    }

    public Hashtable<String, ModifiedArtifact> getModified() {
        return this.modified;
    }

    public void setModified(Hashtable<String, ModifiedArtifact> modified) {
        this.modified = modified;
    }

    public Hashtable<String, RemovedArtifact> getRemoved() {
        return this.removed;
    }

    public void setRemoved(Hashtable<String, RemovedArtifact> removed) {
        this.removed = removed;
    }
}
