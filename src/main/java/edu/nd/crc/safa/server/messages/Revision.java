package edu.nd.crc.safa.server.messages;

import java.util.ArrayList;
import java.util.List;

public class Revision {

    int revision;
    List<TraceChange> traceChanges;
    List<ArtifactChange> artifactChanges;

    public Revision() {
        traceChanges = new ArrayList<>();
        artifactChanges = new ArrayList<>();
    }

    public Revision(int revision,
                    List<TraceChange> traceChanges,
                    List<ArtifactChange> artifactChanges) {
        this.revision = revision;
        this.traceChanges = traceChanges;
        this.artifactChanges = artifactChanges;
    }

    public int getRevision() {
        return revision;
    }

    public void setRevision(int revision) {
        this.revision = revision;
    }

    public List<TraceChange> getTraceChanges() {
        return traceChanges;
    }

    public void setTraceChanges(List<TraceChange> traceChanges) {
        this.traceChanges = traceChanges;
    }

    public List<ArtifactChange> getArtifactChanges() {
        return artifactChanges;
    }

    public void setArtifactChanges(List<ArtifactChange> artifactChanges) {
        this.artifactChanges = artifactChanges;
    }
}
