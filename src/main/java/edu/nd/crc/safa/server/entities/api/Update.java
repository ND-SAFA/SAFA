package edu.nd.crc.safa.server.entities.api;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;

public class Update {

    String type;
    List<TraceAppEntity> traces;
    List<ArtifactAppEntity> artifacts;

    public Update() {
        traces = new ArrayList<>();
        artifacts = new ArrayList<>();
    }

    public Update(String type) {
        this();
        this.type = type;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public List<TraceAppEntity> getTraces() {
        return traces;
    }

    public void setTraces(List<TraceAppEntity> traces) {
        this.traces = traces;
    }

    public List<ArtifactAppEntity> getArtifacts() {
        return artifacts;
    }

    public void setArtifacts(List<ArtifactAppEntity> artifacts) {
        this.artifacts = artifacts;
    }
}
