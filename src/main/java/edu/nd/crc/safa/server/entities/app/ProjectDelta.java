package edu.nd.crc.safa.server.entities.app;

import java.util.Hashtable;
import java.util.List;

public class ProjectDelta {
    Hashtable<String, AddedArtifact> added;
    Hashtable<String, ModifiedArtifact> modified;
    Hashtable<String, RemovedArtifact> removed;
    List<ArtifactAppEntity> missingArtifacts;

    public ProjectDelta() {
    }

    public ProjectDelta(Hashtable<String, AddedArtifact> added,
                        Hashtable<String, ModifiedArtifact> modified,
                        Hashtable<String, RemovedArtifact> removed,
                        List<ArtifactAppEntity> missingArtifacts) {
        this.added = added;
        this.modified = modified;
        this.removed = removed;
        this.missingArtifacts = missingArtifacts;
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

    public List<ArtifactAppEntity> getMissingArtifacts() {
        return this.missingArtifacts;
    }

    public void setMissingArtifacts(List<ArtifactAppEntity> missingArtifacts) {
        this.missingArtifacts = missingArtifacts;
    }
}
